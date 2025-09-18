import os
import sys
import argparse
from dotenv.main import load_dotenv
from google import genai
from google.genai import types

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run a prompt wih optional verbose logging."
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="The user prompt of the model"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging (shows prompt and token counts)"
    )
    return parser.parse_args()

def main():
    # Load environment variables
    load_dotenv()

    # Load the Gemini API key from the environment variables
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)
        
    # Parse CLI arguments
    args = parse_args()
    user_prompt = args.prompt
    verbose = args.verbose

    # Initialize the Gemini client using the provided API key
    client = genai.Client(api_key=api_key)

    # Build messages
    messages = [
        types.Content(role="user", parts=[types.Part(text = user_prompt)])
    ]

    # Calling gemini-model
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents= messages,
    )

    # Text o/p of the model
    print(response.text)

    # Verbose logging
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()