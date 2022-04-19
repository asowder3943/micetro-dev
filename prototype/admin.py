from django.contrib import admin
from prototype.models import *

class CustomAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Experiment, CustomAdmin)
admin.site.register(ExperimentGroup, CustomAdmin)
admin.site.register(Cage, CustomAdmin)
admin.site.register(Mouse, CustomAdmin)
admin.site.register(Measurement, CustomAdmin)
admin.site.register(ExperimentTask, CustomAdmin)
admin.site.register(TumorMeasurement, CustomAdmin)