from django.contrib import admin
from .models import Group, Person, Question, Assessment


# -----------------------------
# Group Admin
# -----------------------------
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


# -----------------------------
# Person Admin
# -----------------------------
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'group', 'total_score')
    list_filter = ('group',)
    search_fields = ('nickname',)
    ordering = ('group', 'nickname')


# -----------------------------
# Question Admin
# -----------------------------
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ('text',)
    ordering = ('id',)


# -----------------------------
# Assessment Admin
# -----------------------------
@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'assessor', 'question', 'score', 'created_at')
    list_filter = ('question', 'score', 'assessor__group')
    search_fields = ('assessor__nickname', 'question__text')
    ordering = ('assessor__group', 'assessor',)
    autocomplete_fields = ('assessor', 'question')
    date_hierarchy = 'created_at'
