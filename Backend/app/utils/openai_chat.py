# app/utils/openai_chat.py
from app.config import OpenAIclient

def get_openai_response(prompt: str, model: str = "gpt-5-nano") -> str:
    """
    Sends a prompt to the OpenAI Chat Completions API and returns the response text.
    """
    try:
        # Different models have different parameter support
        request_params = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        
        # Only add temperature for models that support it
        if model not in ["gpt-5-nano"]:
            request_params["temperature"] = 0.7
            
        resp = OpenAIclient.chat.completions.create(**request_params)
         
        # Return the text of the first choice
        return resp.choices[0].message.content.strip()
     
    except Exception as e:
        raise RuntimeError(f"OpenAI API request failed: {e}")