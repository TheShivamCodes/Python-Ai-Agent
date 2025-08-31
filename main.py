import os
import sys #For cli argument
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python
from functions.write_file import schema_write_file
from functions.call_functions import call_functions

# Avallable functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file,
    ]
)

#1. Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# 9. System prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. 
You do not need to specify the working directory in your function calls 
as it is automatically injected for security reasons.
"""


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
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools = [available_functions],
    )
)

# 6,9. Print token usage (prompt + response)
if verbose:
    print(f"\nUser prompt: {user_prompt}") # 9.Additional info only if verbose enabled
    print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"\nResponse tokens: {response.usage_metadata.candidates_token_count}")

# 5. Print the model's text response
print("\nModel Response:")
#print(response.text)
"""
if response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        if part.function_call:
            function_call_part = part.function_call
            print(f"Calling functions: {function_call_part.name}({function_call_part.args})")
            break
        else:
            print(response.text)
else:
    print(response.text)
"""

if response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        if part.function_call:
            function_call_part = part.function_call
            # Call our dispatcher
            function_call_result = call_functions(function_call_part, verbose=verbose)

            # Make sure we got a valid response
            if not function_call_result.parts[0].function_response.response:
                raise RuntimeError("Fatal: No function response returned")

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                print("-> Function executed.")
            break
    else:
        print(response.text)
else:
    print(response.text)

