from fullGSapi.api.client import GradescopeClient
from fullGSapi.api.assignment_grader import GS_assignment_Grader as Grader
from fullGSapi.api.assignment_grader import GS_Question as Question
from getpass import getpass
from inspect import getmembers, isfunction
import json

email = "shomil@berkeley.edu"
password = getpass("Gradescope Password:")

# Set these values based on assignment
course_id = 290298
assignment_id = input("assignment_id:")

# Get a handle to the CS 61C Gradescope Client
client = GradescopeClient()
result = client.log_in(email=email, password=password)

# Fetch the question ID corresponding to the feedback question (last question in assignment)
grader = Grader(client=client, course_id=course_id, assignment_id=assignment_id)
feedback_question = grader.get_rubrics().get('questions')[-1]
rubric_item = feedback_question.get('rubric_items')[0].get('id')
question_id = feedback_question.get('id')

submissions = grader.sub_id_to_questions_id()

print('scraping...')

rows = []
for i, row in enumerate(submissions.values()):
    print(i)
    submission_id = row.get('9')
    data = client.grading_get_submission_grader(class_id=course_id, question_id=question_id, submission_id=submission_id)
    data = json.loads(data).get('submission').get('answers')
    if data != {}:
        row = ''.join(data.values()).replace('\n', ' ').strip()
        rows.append('- ' + row)
        
print('\n'.join(reversed(sorted(rows, key=lambda s : len(s)))))
