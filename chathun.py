import requests
from config import GROQ_API_KEY, GROQ_CHAT_URL, GROQ_MODEL

def chat_with_groq(messages):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
            "Content-Type": "application/json"
        }
        data = {
            "model": GROQ_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        print("Sending request with headers:", headers)  # Debug line
        print("Request data:", data)  # Debug line
        print("URL:", GROQ_CHAT_URL)  # Debug line
        response = requests.post(GROQ_CHAT_URL, headers=headers, json=data, timeout=15)
        print("Response status code:", response.status_code)  # Debug line
        response.raise_for_status()
        result = response.json()
        print("Response JSON:", result)  # Debug line
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        return "I couldn't process that request. Please try again."
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        print(f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}")
        return "I'm having trouble connecting to the AI service. Please try again later."
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return "An unexpected error occurred. Please try again."