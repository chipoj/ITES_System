from django.contrib import admin
from .actions import export_as_csv
from .models import (ConceptKnowledgeRepository,QuestionQuiz,QuestionScenario,RuleFact,DfUnique,
                        AugmentedSstudentAnswers,SelectQNameQNotesQRequiredQRuleFactIdRFactsAnswer,AskedQuizQuestions,
                        PKnown,LearningMaterial,CorrectScenarioQuestions,AnsweredScenarioQuestions)

# Register your models here.

admin.site.register(ConceptKnowledgeRepository)


admin.site.register(QuestionQuiz)
# class QuestionQuizAdmin(admin.ModelAdmin):
#     list_display=[field.name for field in QuestionScenario._meta.get_fields()]
#     search_fields = ['course_name','question']  # Add fields for searching in the admin interface
#     list_filter=['course_name','question','Competency_level']
#     actions = [export_as_csv]




admin.site.register(QuestionScenario)
# class QuestionScenarioAdmin(admin.ModelAdmin):
#     list_display=[field.name for field in QuestionScenario._meta.get_fields()]
#     search_fields = ['notes','required','Answer']  # Add fields for searching in the admin interface
#     list_filter=['notes','required','competency_level']
#     actions = [export_as_csv]

admin.site.register(RuleFact)
admin.site.register(DfUnique)
admin.site.register(AugmentedSstudentAnswers)
admin.site.register(SelectQNameQNotesQRequiredQRuleFactIdRFactsAnswer)
admin.site.register(AskedQuizQuestions)
admin.site.register(PKnown)
admin.site.register(CorrectScenarioQuestions)

@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'pdf_file')
    search_fields = ('title',)

@admin.register(AnsweredScenarioQuestions)
class AnsweredScenarioQuestionsAdmin(admin.ModelAdmin):
    list_display=[field.name for field in AnsweredScenarioQuestions._meta.get_fields()]
    search_fields = ['student_answer']  # Add fields for searching in the admin interface
    list_filter=['is_answered_correct','student_answer']
    actions = [export_as_csv]