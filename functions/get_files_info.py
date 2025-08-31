import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        #1. Build absolute path to requested directory
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory_abs = os.path.abspath(working_directory)

        #2. Guardrail: prevent escaping working directory
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        #3. Check if it's a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        #4. List directory contents
        results = []
        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                results.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                results.append(f"- {entry}: Error getting info ({str(e)})")

        return "\n".join(results)

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
