import os
import subprocess
import json
from datetime import datetime
from google.genai import types

# Import schemas + Implementations
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file
from functions.web_search import schema_web_search, web_search

# Defining sandbox root (evertyhing must stay inside here)
SAFE_DIR = os.path.abspath("./calculator")

# Security helpers

def safe_join(path):
    # Ensure file stays inside SAFE_DIR
    full_path = os.path.abspath(os.path.join(SAFE_DIR, path))
    if not full_path.startswith(SAFE_DIR):
        raise PermissionError("Access outside sandbox directory isn't allowed")
    return full_path

def confirm_action(action, args):
    # Ask for confimation before dangerous actions
    dangerous = action in ["write_file", run_python_file]
    if dangerous:
        resp = input(f"⚠️ Confirm {action} with {args}? [y/N]: ")
        return resp.lower() == "y"
    return True

def log_action(action, args, result):
    # Log every function call for auditing
    with open("agent.log", "a") as f:
        entry = {
            "time": datetime.utcnow().isoformat(),
            "action": action,
            "args": args,
            "result": str(result)[:500]
        }
        f.write(json.dumps(entry)+ "\n")

def call_functions(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = dict(function_call_part.args)  # make a copy of args

    # Always inject working_directory for safety
    args["working_directory"] = SAFE_DIR

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Map function names -> actual Python functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": lambda **kw: get_file_content(file_path=safe_join(kw["file_path"])),
        "run_python_file": lambda **kw: run_python_file(file_path=safe_join(kw["file_path"]), args=kw.get("args")),
        "write_file": lambda **kw: write_file(file_path=safe_join(kw["file_path"]), content=kw["content"]),
        "web_search": lambda **kw: web_search(query=kw["query"], limit=kw.get("limit", 3)),
    }

    # Actually call the function
    try:
        if function_name not in function_map:
            raise ValueError(f"Unknown function: {function_name}")

        # Confirm dangerous actions
        if not confirm_action(function_name, args):
            result = "Action cancelled by user"
        else:
            result = function_map[function_name](**args)

    except Exception as e:
        result = f"Error: {str(e)}"

    # Log everything
    log_action(function_name, args, result)

    # Wrap in types.Content so model can consume it
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
