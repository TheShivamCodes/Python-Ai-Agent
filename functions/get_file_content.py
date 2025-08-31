import os
from functions.config import MAX_FILE_CONTENT_LENGTH
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        # Build absolute paths
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory_abs = os.path.abspath(working_directory)

        # Guardrail: prevent access outside working directory
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it's a file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read contents
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Truncate if necessary
        if len(content) > MAX_FILE_CONTENT_LENGTH:
            return content[:MAX_FILE_CONTENT_LENGTH] + f'\n[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file inside the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory."
            ),
        },
    ),
)
