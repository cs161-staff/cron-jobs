from src import grade_feedback as feedback


def grade_feedback(request):
    feedback.process(None)
    return {'success': True}
