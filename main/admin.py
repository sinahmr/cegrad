from django.contrib import admin
from main.models import *


class TheMostAdmin(admin.ModelAdmin):
    fields = ['title', 'description']
    list_display = ['title', 'description']


class VoteAdmin(admin.ModelAdmin):
    fields = ['voter', 'candidate', 'the_most']
    list_display = ['voter', 'candidate', 'the_most']


admin.site.register(TheMost, TheMostAdmin)
admin.site.register(Vote, VoteAdmin)
