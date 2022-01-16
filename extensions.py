def handle_extension_request(payload):
    semester = payload['semester']
    data = payload['data']

    print('Add logic to handle extension request here.')
    print('Semester:', semester)
    print('Extension Data:', data)

    return {
        'success': True
    }
