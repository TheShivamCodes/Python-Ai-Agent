import os
import sys #For cli argument
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_functions import call_functions
from functions.web_search import schema_web_search, web_search

# Avallable functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        schema_web_search,
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
- Get the current UTC time directly from the system (no web access needed)

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

# Refactoring for looping for the llm atmax given steps
# Max loop iterations
MAX_STEPS = 20

if verbose:
    print(f"\nUser prompt: {user_prompt}")

for step in range(MAX_STEPS):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        )
    )

    candidate = response.candidates[0]
    model_content = candidate.content
    messages.append(model_content)  # Record what model "said"

    if verbose:
        print(f"\nStep {step+1} ----------------------")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    done = False

    # Check each part of model response
    for part in model_content.parts:
        if part.function_call:
            function_call_part = part.function_call
            function_call_result = call_functions(function_call_part, verbose=verbose)

            # Ensure function returned something
            if not function_call_result.parts[0].function_response.response:
                raise RuntimeError("Fatal: No function response returned")

            # Add tool result into conversation
            messages.append(function_call_result)

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                print("-> Function executed.")
            break
    else:
        # No function call: final response
        print("\nFinal response:")
        if candidate.content.parts and candidate.content.parts[0].text:
            print(candidate.content.parts[0].text)
        else:
            print("(No text returned)")
        done = True

    if done:
        break
