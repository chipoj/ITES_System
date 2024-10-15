import sys
import os
import django
import csv

# Setup Django environment
sys.path.append('/home/josella/myprojects/lms/mylms')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylms.settings')
django.setup()

from class_room.models import AugmentedSstudentAnswers, ConceptKnowledgeRepository, DfUnique, QuestionQuiz, QuestionScenario, RuleFact, SelectQNameQNotesQRequiredQRuleFactIdRFactsAnswer  # Import your model

# Define the database to be used
DATABASE = 'default'  # or 'datawarehouse_db' if you want to use the other database

def load_csv_file(file_path):
    """
    Load and return data from a CSV file.
    """
    data = []
    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)  # Read rows as dictionaries
            for row in reader:
                data.append(row)  # Add each row (as a dictionary) to the data list
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return None

def upload_data_to_db(data):
    """
    Upload data to the database from a CSV data structure.
    """
    print("#############################################################",data)
    if data is None:
        return

    for row in data:
        try:
            obj, created = ConceptKnowledgeRepository.objects.using(DATABASE).update_or_create(
                concept=row['concept'],
                id=row['id'],
                Definition=row['Definition'],
                Explanation=row['Explanation'],
                case_study=row['case_study'],
                Main_Concept=row['Main_Concept'],
                Concept_ID=row['Concept_ID'],
                Rule=row['Rule']
            )
            action = "Created" if created else "Updated"
            print(f"{action}: {obj}")
        except KeyError as e:
            print(f"Missing key in row {row}: {e}")
        except Exception as e:
            print(f"Error processing row {row}: {e}")


def upload_quiz_qs_to_db(data):
    """
    Upload quiz_qs to the database from a CSV data structure.
    """
    print("#############################################################",data)
    if data is None:
        return

    for row in data:
        try:
            obj, created = QuestionQuiz.objects.using(DATABASE).update_or_create(
                course_name=row['course_name'],
                id=row['id'],
                course_short_name=row['course_short_name'],
                quiz_name=row['quiz_name'],
                question=row['question'],
                option_test=row['option_test'],
                is_correct=row['is_correct'],
                Competency_level=row['Competency_level'],
                Column1=row['is_correct'],
                Concept_Knowledge_repository_id=row['Competency_level']
            )
            action = "Created" if created else "Updated"
            print(f"{action}: {obj}")
        except KeyError as e:
            print(f"Missing key in row {row}: {e}")
        except Exception as e:
            print(f"Error processing row {row}: {e}")


def upload_scenario_qs_to_db(data):
    """
    Upload data to the database from a CSV data structure.
    """
    print("#############################################################",data)
    if data is None:
        return

    for row in data:
        try:
            obj, created = QuestionScenario.objects.using(DATABASE).update_or_create(
                name=clean_and_format_string(row['name']),
                id=row['id'],
                notes=clean_and_format_string(row['notes']),
                required=row['required'],
                income_statment_key=row['income_statment_key'],
                concept_link=row['concept_link'],
                competency_level=row['competency_level'],
                Concept_Knowledge_repository_id=row['Concept_Knowledge_repository_id'],
                Course_Name=clean_and_format_string(row['Course_Name']),
                Answer=clean_and_format_string(row['Answer']),
                # rule_fact=None,
            )
            action = "Created" if created else "Updated"
            print(f"{action}: {obj}")
        except KeyError as e:
            print(f"Missing key in row {row}: {e}")
        except Exception as e:
            print(f"Error processing row {row}: {e}")


def upload_select_to_db(data):
    """
    Upload data to the database from a CSV data structure.
    """
    print("#############################################################",data)
    if data is None:
        return

    for row in data:
        try:
            obj, created = SelectQNameQNotesQRequiredQRuleFactIdRFactsAnswer.objects.using(DATABASE).update_or_create(
                name=row['name'],
                notes=row['notes'],
                required=row['required'],
                rule_fact_id=row['rule_fact_id'],
                facts=row['facts'],
                Answer=row['Answer']
            )
            action = "Created" if created else "Updated"
            print(f"{action}: {obj}")
        except KeyError as e:
            print(f"Missing key in row {row}: {e}")
        except Exception as e:
            print(f"Error processing row {row}: {e}")


def upload_rule_fact_to_db(data):
    """
    Upload data to the database from a CSV data structure.
    """
    print("#############################################################",data)
    if data is None:
        return

    for row in data:
        try:
            obj, created = RuleFact.objects.using(DATABASE).update_or_create(
                rule=row['rule'],
                id=row['id'],
                concept=row['concept'],
                facts=row['facts']
                
            )
            action = "Created" if created else "Updated"
            print(f"{action}: {obj}")
        except KeyError as e:
            print(f"Missing key in row {row}: {e}")
        except Exception as e:
            print(f"Error processing row {row}: {e}")


def upload_augumented_to_db(data):
    """
    Upload data to the database from a CSV data structure.
    """
    print("#############################################################",data)
    if data is None:
        return

    for row in data:
        try:
            obj, created = AugmentedSstudentAnswers.objects.using(DATABASE).update_or_create(
                student_answer=row['student_answer'],
                label=row['label']
            )
            action = "Created" if created else "Updated"
            print(f"{action}: {obj}")
        except KeyError as e:
            print(f"Missing key in row {row}: {e}")
        except Exception as e:
            print(f"Error processing row {row}: {e}")


def upload_df_unique_to_db(data):
    """
    Upload data to the database from a CSV data structure.
    """
    print("#############################################################",data)
    if data is None:
        return

    for row in data:
        try:
            obj, created = DfUnique.objects.using(DATABASE).update_or_create(
                student_answer=row['student_answer'],
                label=row['label']
            )
            action = "Created" if created else "Updated"
            print(f"{action}: {obj}")
        except KeyError as e:
            print(f"Missing key in row {row}: {e}")
        except Exception as e:
            print(f"Error processing row {row}: {e}")


def clean_and_format_string(input_string):
    formatted_string = input_string.replace('\n', ' ')
    return formatted_string
if __name__ == "__main__":
    # Path to your CSV file
    file_path = '/home/josella/myprojects/lms/mylms/class_room/questions_scenario_repository_202410022034.csv'
    data = load_csv_file(file_path)
    # upload_data_to_db(data)

    # upload_quiz_qs_to_db(data)

    # upload_scenario_qs_to_db(data)

    # upload_select_to_db(data)

    # upload_rule_fact_to_db(data)

    # upload_augumented_to_db(data)

    # upload_df_unique_to_db(data)