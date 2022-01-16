"""
Autogrades the feedback questions for homework assignments.
"""

import os
from fullGSapi.api.client import GradescopeClient
from fullGSapi.api.assignment_grader import GS_assignment_Grader as Grader
from fullGSapi.api.assignment_grader import GS_Question as Question

GS_EMAIL = os.environ.get("GS_EMAIL")
GS_PASS = os.environ.get("GS_PASS")

def process(request_json):
    assert request_json is not None, "Must pass JSON payload."
    assert 'assignments' in request_json, "assignments must be in JSON payload."
    assert GS_EMAIL is not None and GS_PASS is not None, "GS_EMAIL and GS_PASS must be set as env. vars."
    
    assignments = request_json['assignments']

    # Get a handle to the CS 61C Gradescope Client
    client = GradescopeClient()
    client.log_in(email=GS_EMAIL, password=GS_PASS)

    for row in assignments:
        print('Grading:', row)
        course_id, assignment_id = row['course_id'], row['assignment_id']

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
                print('Error! Failed to grade row:', row)
                print(result.text)
                continue
                
        n = len(seen) - 1
        print(f'Finished grading! Graded {n} submissions in this round.')
        
    return {
        'success': True
    }