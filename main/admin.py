from django.contrib import admin
from main.models import *


class TheMostAdmin(admin.ModelAdmin):
    fields = ['text']
    list_display = ['text']


class VoteAdmin(admin.ModelAdmin):
    fields = ['voter', 'candidate', 'the_most']
    list_display = ['voter', 'candidate', 'the_most']


class CommentAdmin(admin.ModelAdmin):
    fields = ['commenter', 'target', 'text']
    list_display = ['commenter', 'target', 'text']

admin.site.register(TheMost, TheMostAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Comment, CommentAdmin)