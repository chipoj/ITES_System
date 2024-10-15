from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="homepage"),
    path("post/<int:id>/", views.post_detail,name="post_detail"),
    path("create_post/", views.create_post,name="create_post"),
    path("quiz_management/", views.manage_quiz,name="quiz_management"),
    path("add_rule_concept/", views.add_rule_concept,name="add_rule_concept"),
    path('learning_materials/', views.learning_materials_view, name='learning_materials'),
    path('answered_questions/', views.answered_questions, name='answered_questions'),
    path('answered_scenarion_questions/', views.answered_scenarion_questions, name='answered_scenarion_questions'),
    path("answered_scenario_question/<int:id>/", views.answered_scenario_question_by_id,name="answered_scenario_question_by_id"),
    path('add_question_quiz/', views.add_question_quiz, name='add_question_quiz'),
    path('add_scenarion_question/', views.add_scenarion_question, name='add_scenarion_question'),
    path('restart_quiz_and_scenario/', views.restart_quiz_and_scenario, name='restart_quiz_and_scenario'),
]
