from app.utils.openai_chat import get_openai_response

if __name__ == "__main__":
    response = get_openai_response("Hello, how are you?")
    print(response)