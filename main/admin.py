from django.contrib import admin
from main.models import *


class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'profile_picture']
    list_display = ['user_username', 'profile_picture']

    def user_username(self, obj):
        return obj.user.username


class TheMostAdmin(admin.ModelAdmin):
    fields = ['text']
    list_display = ['text']


class VoteAdmin(admin.ModelAdmin):
    fields = ['voter', 'candidate', 'the_most']
    list_display = ['voter_get_name', 'candidate_get_name', 'the_most_get_text']
    list_filter = ['candidate__user', 'the_most']

    def voter_get_name(self, obj):
        return obj.voter.get_name()

    def candidate_get_name(self, obj):
        if not obj.candidate:
            return '-'
        return obj.candidate.get_name()

    def the_most_get_text(self, obj):
        return obj.the_most.text


class CommentAdmin(admin.ModelAdmin):
    fields = ['commenter', 'target', 'text']
    list_display = ['commenter_get_name', 'target_get_name', 'text']

    def commenter_get_name(self, obj):
        return obj.commenter.get_name()

    def target_get_name(self, obj):
        return obj.target.get_name()


class OpinionAdmin(admin.ModelAdmin):
    fields = ['teller', 'subject', 'text']
    list_display = ['teller_get_name', 'subject', 'text']

    def teller_get_name(self, obj):
        return obj.teller.get_name()


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TheMost, TheMostAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Opinion, OpinionAdmin)
