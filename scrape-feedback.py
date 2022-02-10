from fullGSapi.api.client import GradescopeClient
from fullGSapi.api.assignment_grader import GS_assignment_Grader as Grader
import json

from src.sheets import BaseSpreadsheet, Sheet
from tqdm import tqdm

DATABASE = "https://docs.google.com/spreadsheets/d/1xFah6ga8Zzb8NZZZeIOFJI-JJQoZSRQfE1DGwmBvB6c/edit#gid=0"

base = BaseSpreadsheet(DATABASE)

# Fetch the list of assignments
url = input("Assignment URL: ")
course_id = url.split('/courses/')[1].split('/')[0]
assignment_id = url.split('/assignments/')[1].split('/')[0]

# Fetch the configuration (basically, just GS_EMAIL and GS_PASSWORD)
configuration = Sheet(base.get_sheet('configuration')).get_all_records()
environ = {}
for row in configuration:
    environ[row['key']] = row['value']

# Get a handle to the CS 61C Gradescope Client
client = GradescopeClient()
result = client.log_in(
    email=environ['GS_EMAIL'], password=environ['GS_PASSWORD'])

# Fetch the question ID corresponding to the feedback question (last question in assignment)
grader = Grader(client=client, course_id=course_id,
                assignment_id=assignment_id)
feedback_question = grader.get_rubrics().get('questions')[-1]
rubric_item = feedback_question.get('rubric_items')[0].get('id')
question_id = feedback_question.get('id')

submissions = grader.sub_id_to_questions_id()
feedback_q = list(sorted([int(k.split('.')[0])
                  for k in list(submissions.values())[0].keys()]))[-1]

rows = []
for i, row in tqdm(list(enumerate(submissions.values()))):
    submission_id = row.get(str(feedback_q))
    data = client.grading_get_submission_grader(
        class_id=course_id, question_id=question_id, submission_id=submission_id)
    data = json.loads(data).get('submission').get('answers')
    if data != {}:
        rows.append(''.join(data.values()).replace('\n', ' ').strip())

with open('feedback.txt', 'w') as file:
    file.write('\n'.join(reversed(sorted(rows, key=lambda s: len(s)))))
