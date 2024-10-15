from class_room.helper_functions.KNW_Base_Domain_model import TaxationRuleEngine
from class_room.models import RuleFact
import openai
import os
import re
from experta import Fact
import pandas as pd
import ast
import pandas as pd
import random
# from .KNW_Base_Domain_model import TaxationRuleEngine
import configs


# Function to send the student's answer to OpenAI API for fact extraction
def extract_facts(student_answer, combined_facts):
    # with open('KEY2', 'r') as file:
    #     openai.api_key = file.read().strip()

     openai.api_key = configs.OPENAI_API_KEY
   
    
    # Constructing the prompt to ask for specific facts
     prompt = f"""
    You are given a set of facts and a student's answer. The facts are::
     {combined_facts}
    
    
    The student's answer is as follows: {student_answer}
   Please check the student's answer for mentions of the values in the facts,  
   and take note of the concept being tested based on the fact item concept, For each fact item, if an item is mentioned and if 
   the student shows or indicates that the fact item is equal to that value in any way then leave the fact item value as it 
   is otherwise replace the fact item value with 'Non', this also includes fact items which have true or false values,  
   if a fact item is false or true and the student does not prove it  then replace fact item value  with'Non'. 
   Do this for all fact items except for those related to concepts. 
   All fact items written concepts leave the values as they are 
   Return the items in the same format as provided.
   Leave it as one continuous string. Return the same format. Make sure to return all fact items. Do not add anything else.
   Do not include the word 'None' or similar undefined outputs or change the data type that may cause for the None keyword to be added.
   
    """
    
    # Send the request to OpenAI's API
     response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=4096,
    )

     facts= response.choices[0].message.content.strip()
    
    # Use regex to find all Fact items
     fact_items = re.findall(r'Fact\([^)]*\)', facts)

    # Convert to a list of formatted strings
     fact_list = [item.strip() for item in fact_items]
     return fact_list


def extract_taxation_rules(student_facts):
   
    engine = TaxationRuleEngine()
    # engine.reset()

    facts = []

    for fact_str in student_facts:
        fact_args = fact_str.replace("Fact(", "").replace(")", "").strip()

        print(f"Processing fact: {fact_str}")

        args = {}
        for arg in fact_args.split(','):
            try:
                k, v = arg.split('=')
                k = k.strip()
                v = v.strip().strip("'")
                args[k] = v
            except ValueError as e:
                print(f"Error processing argument '{arg}': {e}")

        fact = Fact(**args)
        facts.append(fact)


    engine.declare(*facts)
    engine.run()
    taxation_feedback = engine.get_feedback()

    return taxation_feedback


# Function to prepare and send the OpenAI prompt for NL feedback for the student
def generate_student_feedback(inference_engine_feedback, student_answer, correct_solution):
    # Set your OpenAI API key
    # with open('KEY2', 'r') as file:
    #     openai.api_key = file.read().strip()

     openai.api_key = configs.OPENAI_API_KEY
    # Construct the prompt for OpenAI
     prompt = f"""
    You are a teacher providing feedback on a student's answer to an accounting question. 
    Below is the feedback from an inference engine based on predefined taxation rules, 
    the student's answer, and the correct solution to the question. 
    Please give the student constructive feedback, just as a teacher would. 
    Start by acknowledging what the student did well, and then gently explain the areas where the student 
    can improve based on the taxation rules. 
    Make sure to identify any missed concepts or mistakes based on the taxation rules from the inference engine and the ideal solution,
    and explain the correct reasoning clearly based on the taxation laws that is the values from the inference engine. 
    Do not write as a letter because this feedback will be given within another system. 
    Your ending should encourage the student to retry again if they need to or move to the next question.

    Feedback from the inference engine:
    {inference_engine_feedback}

    The student's answer:
    {student_answer}

    The correct solution to the question:
    {correct_solution}

    Provide feedback to the student in a way that is educational, supportive, and constructive, highlighting areas of improvement.
    If a student has identified more than 50% of the rules from the inference engine and if they have identified more than 50%
    of the concepts, please include "student_correct=True" or "Student_correct=False" if they have not achieved the 50%
    in your response as a separate line.
    """

    # Call the OpenAI API
     response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=4096,
    )

    # Extract and return the feedback from OpenAI's response
     feedback = response.choices[0].message.content.strip()
    
    # Initialize student_correct as False
     student_correct = False
    
    # Check for student_correct in the feedback
     if "student_correct=True" in feedback:
        student_correct = True
        feedback = feedback.replace("student_correct=True", "").strip()
     elif "student_correct=False" in feedback:
        student_correct = False
        feedback = feedback.replace("student_correct=False", "").strip()
    
    # Display the feedback
     print(f"\n{feedback}\n")
     print(f"\n{student_correct}\n")
     return student_correct, feedback


def handle_scenario_question(student_answer,answer_scenario_question):
    print("________________-----------------------________________<>",answer_scenario_question)
    rule_facts = RuleFact.objects.filter(id=answer_scenario_question.rule_fact.id).first()
    #Sending student answers and facts for facts extraction
    print("\nExtracting facts from student response\n")
    student_identified_facts=extract_facts(student_answer, [rule_facts.facts])
    print("The student_identified_facts",student_identified_facts)

    print (f"Feedback based on Taxation rules \n\n")
    inference_engine_rules= extract_taxation_rules(student_identified_facts)
    #Get natural language feedback from OpneAI 
    print("\nFeedback from Teacherbot:\n",inference_engine_rules)
    current_ideal_solutions = answer_scenario_question.Answer
    student_correct, feedback =generate_student_feedback(inference_engine_rules, student_answer, current_ideal_solutions)

    return student_correct,feedback, inference_engine_rules, 

# BKT update function (separate BKT logic)
def update_bkt(correct, P_Known, P_T=0.2, P_G=0.25, P_S=0.1):
    if correct:
        P_Known_given_Correct = (P_Known * (1 - P_S)) / (P_Known * (1 - P_S) + (1 - P_Known) * P_G)
        return P_Known_given_Correct + (1 - P_Known_given_Correct) * P_T
    else:
        P_Known_given_Incorrect = (P_Known * P_S) / (P_Known * P_S + (1 - P_Known) * (1 - P_G))
        return P_Known_given_Incorrect + (1 - P_Known_given_Incorrect) * P_T

# Get input from student and check if correct, provide feedback for quiz questions
def get_student_answer(quiz_name, question, options):
    print(f"\nQuiz: {quiz_name}")
    print(f"Question: {question}")
    
    # Display answer options to the student
    for i, option in enumerate(options):
        print(f"{i + 1}. {option['option_test']}")

    # Get student's answer
    try:
        student_choice = int(input("Select your answer (1/2/3/4): ")) - 1
        if student_choice < 0 or student_choice >= len(options):
            print("Invalid choice. Please select a valid option.")
            return get_student_answer(quiz_name, question, options)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_student_answer(quiz_name, question, options)
    
    # Check if the selected answer is correct
    is_correct = options[student_choice]['is_correct'] == "Correct"
    if is_correct:
        print("Correct! Well done.")
        return True  # The answer is correct
    else:
        # Handle cases where no correct answer is found to prevent StopIteration error
        correct_option = next((option for option in options if option['is_correct'] == "Correct"), None)
        if correct_option:
            print(f"Incorrect. The correct answer was: {correct_option['option_test']}")
        else:
            print("No correct answer found for this question in the database.")
        return False  # The answer is incorrect



# Function to write the rule to the KNW_Base_Domain_model.py file
def write_rule_to_script(concept, fact_name, fact_value, rule_description, feedback_message):
    rule_template = f"""
    @Rule(Fact(concept='{concept}'), Fact({fact_name}='{fact_value}'))
    def {rule_description}(self):
        self.correct = True
        self.rule_fired = True
        message = \"{feedback_message}\"
        self.add_feedback(message)
        print(message)
        """
    
    try:
        with open("class_room/helper_functions/KNW_Base_Domain_model.py", "a") as file:
            file.write(rule_template)
        print(f"Rule '{rule_description}' successfully written to KNW_Base_Domain_model.py.")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
