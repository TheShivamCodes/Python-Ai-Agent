
import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

def call_functions(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = dict(function_call_part.args)  # make a copy of args

    # Always inject working_directory for safety
    args["working_directory"] = "./calculator"

    # Map function names -> actual Python functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Check if the function exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Actually call the function
    try:
        result = function_map[function_name](**args)
    except Exception as e:
        result = f"Error during execution: {str(e)}"

    # Wrap result in a Content -> Part -> FunctionResponse
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
