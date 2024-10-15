from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class ConceptKnowledgeRepository(models.Model):
    concept = models.TextField()
    id = models.IntegerField(primary_key=True)
    Definition = models.TextField()
    Explanation = models.TextField()
    case_study = models.TextField()
    Main_Concept = models.TextField()
    Concept_ID = models.TextField()
    Rule = models.TextField()


class QuestionQuiz(models.Model):
    id = models.IntegerField(primary_key=True)
    course_name = models.TextField()
    course_short_name = models.TextField()
    quiz_name = models.TextField()
    question = models.TextField()
    option_test = models.TextField()
    is_correct = models.TextField()
    Competency_level = models.TextField()
    Column1 = models.CharField(max_length=50)
    Concept_Knowledge_repository_id = models.TextField()

class RuleFact(models.Model):
    id = models.IntegerField(primary_key=True)
    rule = models.TextField()
    concept = models.TextField()
    facts = models.TextField()
    fact_value = models.TextField(null=True, blank=True)
    rule_description = models.TextField(null=True, blank=True)
    feedback_message = models.TextField(null=True, blank=True)

    def __str__(self):
        truncated_rule = self.rule[:30] + '...' if len(self.rule) > 30 else self.rule
        return f"<{self.concept}-{truncated_rule}>"


class QuestionScenario(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    notes = models.TextField()
    required=models.TextField()
    income_statment_key = models.TextField()
    concept_link = models.TextField()
    competency_level = models.TextField()
    Concept_Knowledge_repository_id = models.CharField(max_length=50)
    Course_Name = models.TextField()
    Answer = models.TextField()
    rule_fact = models.ForeignKey(RuleFact, on_delete=models.SET_NULL, null=True, blank=True)


class DfUnique(models.Model):
    student_answer = models.TextField()
    label = models.TextField()



class SelectQNameQNotesQRequiredQRuleFactIdRFactsAnswer(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField()
    required = models.TextField()
    rule_fact_id = models.IntegerField()
    facts = models.TextField()
    Answer = models.TextField()

class AugmentedSstudentAnswers(models.Model):
    student_answer = models.TextField()
    label = models.TextField()


class AskedQuizQuestions(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE, related_name='asked_questions')
    quiz_question = models.ForeignKey(QuestionQuiz,on_delete=models.CASCADE,null=True)
    scenario_question = models.ForeignKey(QuestionScenario,on_delete=models.CASCADE,null=True)

class CorrectScenarioQuestions(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE, related_name='correct_scenario_questions')
    scenario_question = models.ForeignKey(QuestionScenario,on_delete=models.CASCADE,null=True)

class AnsweredScenarioQuestions(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE, related_name='all_answered_scenario_questions')
    scenario_question = models.ForeignKey(QuestionScenario,on_delete=models.CASCADE,null=True)
    student_answer = models.TextField(null=True,blank=True)
    openai_answer = models.TextField(null=True,blank=True)
    student_facts_identified = models.TextField(null=True,blank=True)
    is_answered_correct = models.BooleanField(default=False, null=True,blank=True)

class PKnown(models.Model):
    student = models.OneToOneField(User,on_delete=models.CASCADE, related_name='p_known')
    p_known= models.DecimalField(decimal_places=2,max_digits=6,default=0.3)


class LearningMaterial(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='learning_materials/')
    competency_level = models.IntegerField()

    def __str__(self):
        return self.title