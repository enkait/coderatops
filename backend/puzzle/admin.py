from puzzle.models import Puzzle, Test, PuzzleInstance, Submission
from django.contrib import admin

class TestChoiceInline(admin.TabularInline):
    model = Test
    extra = 3

class PuzzleAdmin(admin.ModelAdmin):
    inlines = [TestChoiceInline]

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 3

class PuzzleInstanceAdmin(admin.ModelAdmin):
    inlines = [SubmissionInline]

admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(PuzzleInstance, PuzzleInstanceAdmin)
