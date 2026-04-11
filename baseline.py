import os
from openai import OpenAI

# The validator INJECTS these variables. If you don't use them, you fail.
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"), 
    api_key=os.environ.get("API_KEY")
)

def get_llm_action(observation):
    """
    This function MUST be called in your loop to satisfy the check.
    """
    try:
        response = client.chat.completions.create(
            model=os.environ.get("LLM_MODEL", "gpt-4o"), # Use the injected model name
            messages=[
                {"role": "system", "content": "You are a traffic controller. Output only 0 or 1."},
                {"role": "user", "content": f"State: {observation}"}
            ]
        )
        content = response.choices[0].message.content
        # Extract the first digit found in the response
        return int(''.join(filter(str.isdigit, content))[0])
    except Exception as e:
        print(f"Proxy Error or Parse Error: {e}")
        return 0 # Fallback
