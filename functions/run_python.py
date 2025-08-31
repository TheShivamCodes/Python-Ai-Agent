import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Build absolute paths
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory_abs = os.path.abspath(working_directory)

        # Guardrail: prevent executing outside working directory
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # File must exist
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        # Must be a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Run the Python file with subprocess
        try:
            completed = subprocess.run(
                ["python", full_path, *args],
                cwd=working_directory_abs,
                capture_output=True,
                text=True,
                timeout=30
            )
        except subprocess.TimeoutExpired:
            return f'Error: Execution of "{file_path}" timed out after 30 seconds'

        # Collect stdout and stderr
        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        output_lines = []

        if stdout:
            output_lines.append("STDOUT:\n" + stdout)
        if stderr:
            output_lines.append("STDERR:\n" + stderr)
        if completed.returncode != 0:
            output_lines.append(f"Process exited with code {completed.returncode}")
        if not output_lines:
            return "No output produced."

        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python script."
            )
        },
        required = ["file_path"]
    )
)
