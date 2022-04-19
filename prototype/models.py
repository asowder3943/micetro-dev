from django.db import models
from pandas import DataFrame
from django.contrib.auth.models import User

class OwnedModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        abstract = True

class Experiment(OwnedModel):
    name = models.TextField(null=False)
    description = models.TextField()

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def just_start_date(self):
        return self.start_date.date()

    def just_end_date(self):
        return self.end_date.date()

    def __str__(self):
        return f"{self.name}"

    def groups(self):
        return ExperimentGroup.objects.filter(experiment=self)

    def cages(self):
        return Cage.objects.filter(experiment=self)

    def mice(self):
        return Mouse.objects.filter(experiment_group__in=self.groups())

    
class ExperimentGroup(models.Model):
    experiment = models.ForeignKey(Experiment, null=False, on_delete=models.CASCADE)
    
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.experiment}"


class Cage(models.Model):
    experiment = models.ForeignKey(Experiment, null=False, on_delete=models.CASCADE)
    cage_number = models.IntegerField()
    external_id = models.TextField()

    def __str__(self):
        return f"{self.cage_number} - {self.experiment}"

    def mice(self):
        return Mouse.objects.filter(cage=self)   

    def mice_list(self):
        return list(self.mice())

    def mice_by_group(self, group):
        return self.mice().filter(experiment_group=group) 

    def mice_by_group_list(self, group):
        mice = self.mice().filter(experiment_group=group)
        string_list = [str(mouse) for mouse in mice]
        r = ''
        for s in string_list:
            r = r + f"{s}, "
        return r[:-2]
    
    def group_lists(self):
        a = []
        for group in self.experiment.groups():
            a.append(self.mice_by_group_list(group))
        return a

class Mouse(models.Model):
    experiment_group = models.ForeignKey(ExperimentGroup, null=False, on_delete=models.CASCADE)
    cage = models.ForeignKey(Cage, null=False, on_delete=models.CASCADE)

    class EarTag(models.TextChoices):
        N = 'N'
        R = 'R'
        L = 'L'
        B = 'B'
        RR = 'RR'
        LL = "LL"
        BB = 'BB'

    ear_tag = models.CharField(max_length=2, choices=EarTag.choices)
    
    experiment_id = models.IntegerField()

    def experiment(self):
        return self.cage.experiment

    def __str__(self):
        return f"{self.experiment_id} - {self.ear_tag}"

    def latest_measurement(self):
        return Measurement.objects.filter(mouse=self).order_by('measurement_time').last()

    def measurements(self):
        return Measurement.objects.filter(mouse=self).order_by('measurement_time')


class Measurement(models.Model):
    mouse = models.ForeignKey(Mouse, null=False, on_delete=models.CASCADE)
    
    def experiment(self):
        return self.mouse.experiment()

    measurement_time = models.DateTimeField()
    tumor_dimension_1 = models.FloatField()
    tumor_dimension_2 = models.FloatField()
    weight = models.FloatField(null=True)
    notes = models.TextField()

    def tumor_volume(self):
        if self.tumor_dimension_1 > self.tumor_dimension_2:
            return self.tumor_dimension_1 * self.tumor_dimension_2 * self.tumor_dimension_2 * 0.5
        else:
            return self.tumor_dimension_2 * self.tumor_dimension_1 * self.tumor_dimension_1 * 0.5

    def just_date(self):
        return self.measurement_time.date()

    def __str__(self):
        return f"{self.measurement_time}: mouse: {self.mouse}, Volume: {self.tumor_volume()}"

    def mice(self):
        return self.objects.order_by().values('mouse').distinct()

    def volume_over_time(self, experiment):
        mice = self.mice(self)
        rows = []
        for m in mice:
            m_id = m['mouse']
            mouse = Mouse.objects.get(id=m_id)
            if mouse.experiment_group.experiment == experiment:
                measurements = self.objects.filter(mouse=mouse)
                for measurement in measurements:
                    row = [measurement.just_date(), measurement.mouse, mouse.experiment_group.name, measurement.tumor_volume()]
                    rows.append(row)
        df = DataFrame(rows, columns=['date', 'subject', 'group', 'volume'])
        return df

class ExperimentTask(models.Model):
    experiment = models.ForeignKey(Experiment, null=False, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    scheduled_time = models.DateTimeField(null=True)
    parent_event = models.ForeignKey("self", on_delete=models.CASCADE, null=True, unique=False, blank=True)

    class TaskStatus(models.TextChoices):
        NotScheduled = 'ND'
        NotStarted = 'NS'
        InProgress = 'IP'
        Complete = 'CP'
        Blocked = 'BK'

    status = models.CharField(max_length=2, choices=TaskStatus.choices)

class TumorMeasurement(ExperimentTask):
    record = models.ForeignKey(Measurement, on_delete=models.CASCADE, null=True, unique=False, blank=True)
