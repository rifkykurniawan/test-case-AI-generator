import os
from dotenv import load_dotenv
from google import genai

# Resolve the path to the .env file in the backend directory
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, "..", ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv()

def list_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY environment variable is not set.")
        return

    print("Initializing Gemini Client...")
    try:
        client = genai.Client(api_key=api_key)
        print("Fetching models...")
        models = client.models.list()
        
        print("\nAvailable Gemini Models:")
        for model in models:
            display_name = getattr(model, "display_name", "N/A")
            print(f"- {model.name} ({display_name})")
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    list_models()
