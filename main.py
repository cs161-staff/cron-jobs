
"""
Autogrades the feedback questions for homework assignments.
"""
import os
from fullGSapi.api.client import GradescopeClient
from fullGSapi.api.assignment_grader import GS_assignment_Grader as Grader
from fullGSapi.api.assignment_grader import GS_Question as Question
from dotenv import load_dotenv

# For local testing, load environment vars from .env file
load_dotenv() 

GS_EMAIL = os.environ.get("GS_EMAIL")
GS_PASS = os.environ.get("GS_PASS")

def process(request_json):
    assert request_json is not None, "Must pass JSON payload."
    assert 'course_id' in request_json, "course_id must be in JSON payload."
    assert 'assignment_id' in request_json, "assignment_id must be in JSON payload."
    assert GS_EMAIL is not None and GS_PASS is not None, "GS_EMAIL and GS_PASS must be set as env. vars."
    
    course_id, assignment_id = request_json['course_id'], request_json['assignment_id']

    # Get a handle to the CS 61C Gradescope Client
    client = GradescopeClient()
    client.log_in(email=GS_EMAIL, password=GS_PASS)

    # Fetch the question ID corresponding to the feedback question (last question in assignment)
    grader = Grader(client=client, course_id=course_id, assignment_id=assignment_id)
    feedback_question = grader.get_rubrics().get('questions')[-1]
    rubric_item = feedback_question.get('rubric_items')[0].get('id')
    question_id = feedback_question.get('id')

    seen = set()
    while True:
        next_sub_id = client.grading_grade_first_ungraded_or_first(class_id=course_id, question_id=question_id)
        if not next_sub_id:
            break
        
        if next_sub_id in seen:
            break
        else:
            seen.add(next_sub_id)
            
        print('Grading', next_sub_id)

        result = client.grading_save(
            class_id=course_id,
            question_id=question_id,
            submission_id=next_sub_id,
            data={"rubric_items": {
                str(rubric_item): {
                    "score": "true"
                }
            }, "question_submission_evaluation": {
                "points": None,
                "comments": None
            }}
        )
        if result.status_code != 200:
            print('Error!')
            print(result.text)
            raise RuntimeError("Grading Failure. HTTP Output:\n\n" + str(result.text))
            
    n = len(seen) - 1
    print(f'Finished grading! Graded {n} submissions in this round.')
    
    return {
        'success': True,
        'message': f'Autograded {n} submissions.'
    }

def grade_feedback(request):
    """
    Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    try:
        return process(request_json)
    except Exception as err:
        return {
            'success': False,
            'error': str(err)
        }
        