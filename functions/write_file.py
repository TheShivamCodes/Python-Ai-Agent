import os

def write_file(working_directory, file_path, content):
    try:
        # Build absolute paths
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory_abs = os.path.abspath(working_directory)

        # Guardrail: prevent writing outside working directory
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure parent directories exist
        parent_dir = os.path.dirname(full_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        # Write file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
