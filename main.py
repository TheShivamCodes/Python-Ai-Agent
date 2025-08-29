import os
import sys #For cli argument
from google import genai
from dotenv import load_dotenv
from google.genai import types

# 1. Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Check if a prompt was provided via command line arguments
if len(sys.argv)<2:
    print("Error : No prompt provided")
    sys.exit(1)

# Detect verbose flag
verbose = "--verbose" in sys.argv

# 7. Define the prompt
user_prompt = " ".join(sys.argv[1:]) if not verbose else " ".join(sys.argv[1:-1])

# 8. Create a new list of messages (types.Content) with the user's prompt
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

# 2. Initialize the Gemini client
client = genai.Client(api_key=api_key)

# 3. Define the model
model_name = "gemini-2.0-flash-001"

# 4. Generate content from the model
response = client.models.generate_content (
    model = model_name,
    contents = messages,
)

# 6,9. Print token usage (prompt + response)
if verbose:
    print(f"\nUser prompt: {user_prompt}") # 9.Additional info only if verbose enabled
    print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"\nResponse tokens: {response.usage_metadata.candidates_token_count}")

# 5. Print the model's text response
print("\nModel Response:")
print(response.text)
