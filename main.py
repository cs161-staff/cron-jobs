from dotenv import load_dotenv
import extensions, grade_feedback

# For local testing, load environment vars from .env file
load_dotenv() 

def handle_extension_request(request):
    request_json = request.get_json()
    try:
        return extensions.handle_extension_request(request_json)
    except Exception as err:
        return {
            'success': False,
            'error': str(err)
        }

def grade_feedback(request):
    request_json = request.get_json()
    try:
        return grade_feedback.process(request_json)
    except Exception as err:
        return {
            'success': False,
            'error': str(err)
        }
        