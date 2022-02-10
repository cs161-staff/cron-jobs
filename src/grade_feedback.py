"""
Autogrades the feedback questions for homework assignments.
"""

from fullGSapi.api.client import GradescopeClient
from fullGSapi.api.assignment_grader import GS_assignment_Grader as Grader

from src.sheets import BaseSpreadsheet, Sheet

DATABASE = "https://docs.google.com/spreadsheets/d/1xFah6ga8Zzb8NZZZeIOFJI-JJQoZSRQfE1DGwmBvB6c/edit#gid=0"


def process(request_json):

    base = BaseSpreadsheet(DATABASE)

    # Fetch the list of assignments
    assignments = []
    for row in Sheet(base.get_sheet('assignments')).get_all_records():
        url = str(row['url'])
        course_id = url.split('/courses/')[1].split('/')[0]
        assignment_id = url.split('/assignments/')[1].split('/')[0]
        assignments.append((course_id, assignment_id, url))

    # Fetch the configuration (basically, just GS_EMAIL and GS_PASSWORD)
    configuration = Sheet(base.get_sheet('configuration')).get_all_records()
    environ = {}
    for row in configuration:
        environ[row['key']] = row['value']

    # Get a handle to the CS 61C Gradescope Client
    client = GradescopeClient()
    client.log_in(email=environ['GS_EMAIL'], password=environ['GS_PASSWORD'])

    error = False

    # Grade all assignments
    for course_id, assignment_id, url in assignments:
        print(f'Grading assignment: {url}')

        # Fetch the question ID corresponding to the feedback question (last question in assignment).
        grader = Grader(client=client, course_id=course_id,
                        assignment_id=assignment_id)
        feedback_question = grader.get_rubrics().get('questions')[-1]
        rubric_item = feedback_question.get('rubric_items')[0].get('id')
        question_id = feedback_question.get('id')

        seen = set()
        while True:
            next_sub_id = client.grading_grade_first_ungraded_or_first(
                class_id=course_id, question_id=question_id)
            if not next_sub_id:
                break

            if next_sub_id in seen:
                break
            else:
                seen.add(next_sub_id)

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
                error = f'Error: failure occurred while grading assignment: {url} (failure: {result.text})'
                print(error)
                continue

        n = len(seen) - 1
        print(
            f'Finished grading this assignment! Graded {n} submissions in this round.')

    if error:
        raise Exception(error)
