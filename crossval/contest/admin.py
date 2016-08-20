from django.contrib import admin
from contest import models


@admin.register(models.ScoreSchemes)
class ScoreSchemesAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Contest)
class ContestAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('contest', 'public')
    list_order = ('contest', 'public')

@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Submission)
class SubmisisonAdmin(admin.ModelAdmin):
    pass
