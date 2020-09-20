def create_response(result):
    message = "Broken image found"
    if result == '[]':
        message = "Broken image not found"
    response = {
        'Message': message,
        'Result':result
    }
    return response