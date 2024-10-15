from django.shortcuts import render,redirect

from .models import AnsweredScenarioQuestions, AskedQuizQuestions, CorrectScenarioQuestions, LearningMaterial, PKnown, QuestionQuiz, QuestionScenario, RuleFact
from django.shortcuts import get_object_or_404
from django.db.models import Count
# from .forms import PostCreationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .helper_functions.helper_functions import extract_taxation_rules, generate_student_feedback, update_bkt, write_rule_to_script, extract_facts,handle_scenario_question
from collections import defaultdict
from django.core.paginator import Paginator
from django.contrib import messages

import csv
from io import TextIOWrapper
from django.http import HttpResponse

# Create your views here.


def index(request):
    # asked_quiz_questions=AskedQuizQuestions.objects.all()
    asked_quiz_questions=[]
    return render(request, "class_room/index.html",{"asked_quiz_questions":asked_quiz_questions})


def post_detail(request,id):
    # asked_quiz_questions = AskedQuizQuestions.objects.get(id=id)
    asked_quiz_questions={}
    context={
        'asked_quiz_questions':"asked_quiz_questions",
        'title':"asked_quiz_questions.quiz_question"
    }
    return render(request,"class_room/detail.html",context)


@login_required
def create_post(request):
    # form = PostCreationForm()
    # if request.method == "POST":
    #     form = PostCreationForm(request.POST)

        # if form.is_valid():
        #     form_obj = form.save(commit=False)

        #     form_obj.author = request.user

        #     form_obj.save()

        #     return redirect(reverse('homepage'))
    context = {
        # 'form':form
    }
    return render(request,'class_room/createpost.html',context)


def restart_quiz_and_scenario(request):
    profile = request.user.profile
    profile.competency_level = 1
    profile.save()

    new_p_known = request.user.p_known
    new_p_known.p_known = 0.3
    new_p_known.save()

    asked_qs = AskedQuizQuestions.objects.filter(student=request.user)
    if asked_qs:
        for q in asked_qs:
            q.delete()

    correct_scenarios = CorrectScenarioQuestions.objects.filter(student=request.user)
    if correct_scenarios:
        for scenario in correct_scenarios:
            scenario.delete()
    
    all_answered_scenarios = AnsweredScenarioQuestions.objects.filter(student=request.user)
    if all_answered_scenarios:
        for scenario in all_answered_scenarios:
            scenario.delete()

    return redirect(reverse('quiz_management'))

@login_required
def manage_quiz(request):

    competency_level = int(request.user.profile.competency_level)
    p_known_instance, created = PKnown.objects.get_or_create(student=request.user, defaults={'p_known': 0.3})
    # Access p_known
    P_Known = p_known_instance.p_known
    print(competency_level,P_Known)
    # Define initial BKT parameters
    mastery_threshold = 0.8  # Mastery threshold
    max_competency_level = 10  # Max level of complexity in the quiz
    current_level = competency_level  # Starting level based on input
    max_scenario_questions = 10  # Maximum scenario-based questions to attempt
    context = {}
    # Check if competency level is greater than or equal to max
    if competency_level >= max_competency_level:
        context = {
                "competency_level":competency_level,
                "p_known": P_Known,
            }
        messages.info(request,"You have mastered the Course")
        return render(request,'class_room/answer_quiz.html',context)

    if current_level <= max_competency_level:
    
        # Get the list of quiz questions that have already been asked
        asked_quiz_questions = AskedQuizQuestions.objects.filter(student=request.user).values_list('quiz_question_id', flat=True)
        
        if request.method == 'POST':
            # 1st check if its a quiz or a scenario
            question_type = request.POST.get('question_type', None)

            if question_type: 

                notes = request.POST['notes']
                required = request.POST['required']
                student_answer = request.POST['open_ended_answer']             
                
                answer_scenario_question = QuestionScenario.objects.filter(competency_level=competency_level, notes = notes,required=required).first()
                # Process the scenario question
                if answer_scenario_question is None:
                    print("No Question for your competency_level=competency_level, notes = notes,required=required")
                    return redirect(reverse('quiz_management'))
                student_correct,feedback, student_identified_facts,  =handle_scenario_question(student_answer,answer_scenario_question)
                

                save_scenario, created = AnsweredScenarioQuestions.objects.update_or_create(student = request.user,
                                                                            scenario_question = answer_scenario_question,
                                                                            student_answer=student_answer,
                                                                            openai_answer=feedback,
                                                                            is_answered_correct=student_correct,
                                                                            student_facts_identified=student_identified_facts)
                


                # Track the correct responses
                if student_correct:
                    P_Known = update_bkt(True, float(P_Known))
                    correct_scenario = CorrectScenarioQuestions.objects.create(student = request.user,scenario_question = answer_scenario_question)
                    correct_scenario.save()

                
                    
                else:
                    P_Known = update_bkt(False, float(P_Known))

                # Update BKT based on response
                p_known_instance.p_known = P_Known
                p_known_instance.save()

                #save to Asked Questions
                current_asked_question = AskedQuizQuestions.objects.create(
                        student=request.user,
                        scenario_question=answer_scenario_question
                    )
                current_asked_question.save()

                correct_scenario_count = CorrectScenarioQuestions.objects.all().count()
                
                # If student masters scenario-based questions, end the program with congratulations
                if correct_scenario_count >= max_scenario_questions:
                    print("\nCongratulations! You have mastered the scenario-based questions and completed the highest level of the quiz.")
                    messages.success(request,'Congratulations! You have mastered the scenario-based questions and completed the highest level of the quiz.')
                    context = {
                            "competency_level":competency_level,
                            "p_known": P_Known,
                        }
                    return render(request,'class_room/answer_quiz.html',context)
                
                asked_quiz_questions = AskedQuizQuestions.objects.filter(student=request.user).exclude(scenario_question__isnull=True).values_list('scenario_question_id', flat=True)

                # Use the filtered IDs in the next query
                next_quiz_question = QuestionScenario.objects.filter(competency_level=competency_level).exclude(id__in=asked_quiz_questions).first()
                                    

                if next_quiz_question is not None:
                    # Get the next Scenario
                    context = {
                            "show_modal": True,
                            "feedback": feedback,
                            "student_identified_facts":student_identified_facts,
                            "quiz_name":next_quiz_question.name,
                            "scenario": next_quiz_question.notes,
                            "question":next_quiz_question.required,
                            "competency_level":competency_level,
                            "p_known": P_Known,
                            "question_type":True if competency_level>1 else False  # True when the student is moving to scenario based
                        }
                    
                    return render(request,'class_room/answer_quiz.html',context)
                     
            if question_type is None:
                answer = request.POST['answer']
                quiz_name = request.POST['quiz_name']
                question = request.POST['question']
                actual_answer = request.POST['actual_answer']

                answer_quiz_question = QuestionQuiz.objects.filter(Competency_level=competency_level, quiz_name = quiz_name,question=question, option_test=answer).first()
                if answer_quiz_question.is_correct == "Correct":
                    student_response=True
                else:
                    student_response=False

                # Update BKT based on response
                P_Known = update_bkt(student_response, float(P_Known))
                p_known_instance.p_known = P_Known
                p_known_instance.save()

                
                print(f"Updated P(Known) after this quiz question: {P_Known:.4f}")


                # If the student has mastered the skill, move to scenario-based questions
                if P_Known >= mastery_threshold:
                    profile = request.user.profile
                    profile.competency_level= ( competency_level + 1)
                    profile.save()
                    print(f"Student has mastered level {current_level} in quizzes. Moving to scenario-based questions.")
                    scenario_mastered = False
                    msg=f"You have mastered level {current_level} in quizzes. Moving to scenario-based questions."
                    messages.success(request,msg)


                # saving the recently asked and answered question
                quiz_questions = QuestionQuiz.objects.filter(
                    Competency_level=competency_level,
                    quiz_name=quiz_name,
                    question=question
                ).exclude(id__in=asked_quiz_questions)

                for current_asked in quiz_questions:
                    current_asked_question = AskedQuizQuestions.objects.create(
                        student=request.user,
                        quiz_question=current_asked
                    )
                    current_asked_question.save()


            return redirect(reverse('quiz_management'))

        #When the request method is not POST            
        else:
            # Get the first QuestionQuiz that has not been asked
            if competency_level<2:
                first_quiz_question = QuestionQuiz.objects.filter(Competency_level=competency_level).exclude(id__in=asked_quiz_questions).first()
                if first_quiz_question is not None:
                    # Get all questions with the same quiz_name and question as the first quiz question
                    quiz_questions = QuestionQuiz.objects.filter(
                        Competency_level=competency_level,
                        quiz_name=first_quiz_question.quiz_name,
                        question=first_quiz_question.question
                    ).exclude(id__in=asked_quiz_questions)

                    context = {
                        "quiz_name":first_quiz_question.quiz_name,
                        "question": first_quiz_question.question,
                        "options":[option.option_test for option in quiz_questions],
                        "is_correct":[option.is_correct for option in quiz_questions],
                        "competency_level":competency_level,
                        "p_known": P_Known,
                    }
                    
                    print("Correct Answer _______----------------____:",[option.is_correct for option in quiz_questions])


                    return render(request,'class_room/answer_quiz.html',context)

                else:
                    messages.warning(request,'Could not Find more questions for your Competency Level, Restart Quiz')
                    context = {
                            "competency_level":competency_level,
                            "p_known": P_Known,
                        }
                    return render(request,'class_room/answer_quiz.html',context)


            elif P_Known < mastery_threshold or competency_level>1 : #when competency is 2 or more meaning we are now dealinging with scenario

                asked_quiz_questions = AskedQuizQuestions.objects.filter(student=request.user).exclude(scenario_question__isnull=True).values_list('scenario_question_id', flat=True)

                # Use the filtered IDs in the next query
                first_quiz_question = QuestionScenario.objects.filter(competency_level=competency_level).exclude(id__in=asked_quiz_questions).first()

                if not first_quiz_question and competency_level > 1:
                    msg = f"You have Successfully Mastered the questions for {competency_level}"
                    messages.success(request,msg) 
                    profile = request.user.profile
                    profile.competency_level = ( competency_level + 1)
                    profile.save()

                    return redirect(reverse('quiz_management'))

                                    

                if first_quiz_question is not None:
                    # Get the next Scenario
                    context = {
                            "quiz_name":first_quiz_question.name,
                            "scenario": first_quiz_question.notes,
                            "question":first_quiz_question.required,
                            "competency_level":competency_level,
                            "p_known": P_Known,
                            "question_type":True if competency_level>1 else False  # True when the student is moving to scenario based
                        }
                    
                    return render(request,'class_room/answer_quiz.html',context)
        
                #case were all the questions have finished
                else:
                    messages.success(request,"You have Successfully Mastered the questions") 
                    context = {
                            "competency_level":competency_level,
                            "p_known": P_Known,
                        }
                    return render(request,'class_room/answer_quiz.html',context)
            

            # When now answering Scenario based Questions
            # if P_Known >= mastery_threshold or competency_level>=2:
                
            #     last_asked_question = AskedQuizQuestions.objects.filter(student=request.user).last()
                
            #     next_question = None
                
            #     if last_asked_question:
            #         # Get the last asked quiz question ID and retrieve the corresponding QuestionScenario
            #         try:
            #             last_question_scenario = get_object_or_404(QuestionScenario, id=last_asked_question.scenario_question_id)
            #             print("Apa----11")
            #         except Exception as e:
            #             last_question_quiz = get_object_or_404(QuestionQuiz, id=last_asked_question.quiz_question_id)
            #             print("Apa----10")

            #         # Filter questions that have the same 'required_field' as the last asked question
            #         try:
            #             related_questions = QuestionScenario.objects.filter(competency_level=competency_level,notes=last_question_scenario.notes).exclude(id__in=asked_quiz_questions)
            #             print("Apa----9")
            #         except Exception as e:
            #             print(e)
            #             related_questions= None
            #             print("Apa----8")

            #         # If there are related questions, get the first one
            #         if related_questions:
            #             next_question = related_questions.first()
            #             print("Apa----7")
            #         else:
            #             # If no related questions, get the next question based on the competency level
            #             next_question = QuestionScenario.objects.filter(competency_level=competency_level).exclude(id__in=asked_quiz_questions).first()
            #             print("Apa----6")
            #         print("--------",next_question)
            #         context = {
            #                 "quiz_name":next_question.name,
            #                 "scenario": next_question.notes,
            #                 "question":next_question.required,
            #                 "competency_level":competency_level,
            #                 "p_known": P_Known,
            #                 "question_type":True if P_Known >= mastery_threshold else False  # True when the student is moving to scenario based
            #             }
                # else:
                #     messages.warning(request,"No Previous Questions Asked on this competency Level")
                #     return redirect(reverse('quiz_management'))
            

                # #case were all the questions have finished
                # if not next_question:
                #     messages.success(request,"You have Successfully Mastered the questions") 
                    
                #     return redirect(reverse('homepage'))

                
                # this return is for both quize and scenario
                # return render(request,'class_room/answer_quiz.html',context)
            
            
                    

            # return render(request,'class_room/answer_quiz.html',context)

            
        


@login_required
def answered_questions(request):
    # Group asked quiz questions by quiz_name and question
    grouped_asked_quiz_questions = (
        AskedQuizQuestions.objects
        .filter(student=request.user)
        .values('quiz_question__quiz_name', 'quiz_question__question')
        .annotate(question_count=Count('quiz_question'))
    )

    questions = []
    # Output each group
    for group in grouped_asked_quiz_questions:
        quiz_name = group['quiz_question__quiz_name']
        question = group['quiz_question__question']
        count = group['question_count']
        print(f"Quiz Name: {quiz_name}, Question: {question}, Count: {count}")
        questions.append(group)


    return render(request,'class_room/answered_questions.html',{"questions":questions})


@login_required
def answered_scenarion_questions(request):
    # Group asked quiz questions by quiz_name and question
    questions = AnsweredScenarioQuestions.objects.filter(student=request.user)

    return render(request,'class_room/answeres_scenarion_question.html',{"questions":questions})

@login_required
def answered_scenario_question_by_id(request,id):
    # Group asked quiz questions by quiz_name and question
    question = AnsweredScenarioQuestions.objects.filter(student=request.user,pk=id).last()

    return render(request,'class_room/view_scenario_answered_question.html',{"answered_question":question})

@login_required
def add_rule_concept(request):
    if request.method == 'POST':
        concept = request.POST['concept']
        fact_name = request.POST['fact_name']
        fact_value = request.POST['fact_value']
        rule_description = request.POST['rule_description']
        feedback_message = request.POST['feedback_message']

        for key in request.POST.keys():
            print(request.POST[key])

        write_rule_to_script(concept, fact_name, fact_value, rule_description, feedback_message)

        # Create a new RuleFact object and save it to the database
        rule_fact = RuleFact(
            concept=concept,
            facts=fact_name,
            fact_value=fact_value,
            rule_description=rule_description,
            feedback_message=feedback_message
        )
        rule_fact.save()
        messages.success(request, "Rules added successfully!")
        return redirect('add_rule_concept') 

    else:
        # Fetch all RuleFact objects
        rules_list = RuleFact.objects.all()

        # Paginate the rules (10 rules per page)
        paginator = Paginator(rules_list, 10)  # Show 10 rules per page
        page_number = request.GET.get('page')  # Get the current page number from the request
        page_obj = paginator.get_page(page_number)  # Get the relevant page of rules

        return render(request, 'class_room/add_rule_concept.html', {'page_obj': page_obj})

@login_required
def learning_materials_view(request):
    competency_level = request.user.profile.competency_level
    # Filter learning materials based on the competency level (less than or equal to)
    materials = LearningMaterial.objects.filter(competency_level__lte=competency_level)
    # Group materials by competency level
    grouped_materials = defaultdict(list)
    for material in materials:
        grouped_materials[material.competency_level].append(material)

    # Create a sorted list of tuples (competency level, materials list)
    sorted_materials = sorted(grouped_materials.items(), key=lambda x: x[0])

    return render(request, 'class_room/learning_material.html', {
        'materials': sorted_materials,
        'competency_level': competency_level,
    })


@login_required
def add_question_quiz(request):
    if request.method == "POST":
        # Check if the form for adding a single question is submitted
        if 'add_question' in request.POST:
            question_id = get_next_id()
            # Process form data
            question = QuestionQuiz(
                id=question_id,
                course_name=request.POST.get('course_name'),
                course_short_name=request.POST.get('course_short_name'),
                quiz_name=request.POST.get('quiz_name'),
                question=request.POST.get('question'),
                option_test=request.POST.get('option_test'),
                is_correct=request.POST.get('is_correct'),
                Competency_level=request.POST.get('competency_level'),
                Column1=request.POST.get('column1'),
                Concept_Knowledge_repository_id=request.POST.get('concept_knowledge_repository_id')
            )
            question.save()
            messages.success(request, "questions added successfully!")
        
        # Check if the CSV upload form is submitted
        elif 'upload_csv' in request.POST and request.FILES['csv_file']:
            csv_file = request.FILES['csv_file']
            # Process the uploaded CSV file
            file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(file_data)
            
            for row in reader:
                question_id = get_next_id()
                # For each row, create a new QuestionQuiz object and save it
                QuestionQuiz.objects.create(
                    id=question_id,
                    course_name=row['course_name'],
                    course_short_name=row['course_short_name'],
                    quiz_name=row['quiz_name'],
                    question=row['question'],
                    option_test=row['option_test'],
                    is_correct=row['is_correct'],
                    Competency_level=row['Competency_level'],
                    Column1=row['Column1'],
                    Concept_Knowledge_repository_id=row['Concept_Knowledge_repository_id']
                )
            messages.success(request, "CSV file uploaded and questions added successfully!")

    return render(request, 'class_room/add_question_quiz.html')

login_required
def add_scenarion_question(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        notes = request.POST.get('notes')
        required = request.POST.get('required')
        income_statement_key = request.POST.get('income_statement_key')
        concept_link = request.POST.get('concept_link')
        competency_level = request.POST.get('competency_level')
        concept_knowledge_repository_id = request.POST.get('concept_knowledge_repository_id')
        course_name = request.POST.get('course_name')
        answer = request.POST.get('answer')
        rule_fact_id = request.POST.get('rule_fact')

        rule_fact = RuleFact.objects.get(id=rule_fact_id) if rule_fact_id else None

        question_scenario = QuestionScenario(
            name=name,
            notes=notes,
            required=required,
            income_statment_key=income_statement_key,
            concept_link=concept_link,
            competency_level=competency_level,
            Concept_Knowledge_repository_id=concept_knowledge_repository_id,
            Course_Name=course_name,
            Answer=answer,
            rule_fact=rule_fact
        )
        question_scenario.save()
        messages.success(request,'Congratulations! You have mastered the scenario-based questions and completed the highest level of the quiz.')

    # If GET request, render the form
    return render(request, 'class_room/add_scenario_question.html', {'rule_facts': RuleFact.objects.all()})

def get_next_id():
    # Get the maximum ID in the table and increment by 1
    max_id = QuestionQuiz.objects.order_by('-id').first()
    return max_id.id + 1 if max_id else 1  # Return 1 if table is empty