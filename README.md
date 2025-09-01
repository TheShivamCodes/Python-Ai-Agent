# Ai-Agent
Ai-Agent is an experimental AI-powered agent capable of interacting with your filesystem, running Python code, reading/writing files, performing web searches, and automating tasks. It is designed for learning and prototyping AI agents, not for production use.

---

## Project Structure

Ai-Agent
├─ calculator
│ ├─ pkg
│ │ ├─ calculator.py
│ │ └─ render.py
│ ├─ README.md
│ ├─ calculate.py
│ ├─ list_example.py
│ ├─ main.py
│ └─ tests.py
├─ functions
│ ├─ call_functions.py
│ ├─ config.py
│ ├─ get_file_content.py
│ ├─ get_files_info.py
│ ├─ run_python.py
│ ├─ web_search.py
│ └─ write_file.py
├─ LICENSE
├─ README.md
├─ agent.log
├─ main.py
├─ pyproject.toml
├─ tests.py
└─ uv.lock

---

## Features

The Ai-Agent can:

- **List files and directories** (`get_files_info`)
- **Read file contents** (`get_file_content`)
- **Execute Python scripts with optional arguments** (`run_python_file`)
- **Write or overwrite files** (`write_file`)
- **Perform web searches** (`web_search`)

All operations are safely scoped to a working directory to prevent accidental system-wide changes.

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/TheShivamCodes/Python-Ai-Agent
cd Ai-Agent

Note:
A virtual environment (venv) is a lightweight, isolated Python environment that allows you to manage dependencies for a specific project without interfering with your system Python or other projects. Here’s why it’s useful and why you need the commands:

->Why Use venv

1. Isolation of Dependencies
Each project can have its own versions of packages without affecting other projects or your system Python.

2. Reproducibility
Other developers can recreate the same environment with the same packages, avoiding “it works on my machine” problems.

3. Safety
Installing packages globally can break system tools or other projects. Using a virtual environment keeps things contained.

->Key Commands

Create a virtual environment

python3 -m venv .venv

Creates a .venv folder in your project directory containing an isolated Python environment.

Activate the virtual environment

macOS/Linux (bash, zsh):
source .venv/bin/activate

Windows (PowerShell):
.venv\Scripts\Activate.ps1

After activation, your shell prompt usually shows the environment name, e.g., (.venv) $.

Install dependencies inside the venv using uv or pip

uv add google-genai==1.12.1
uv add python-dotenv==1.1.0
uv add bs4

This installs the required packages only inside the virtual environment.

Deactivate the environment:
deactivate

Returns your shell to the system Python environment.

Create a .env file in the project root and set your Gemini API key:

env
GEMINI_API_KEY=your_api_key_here


Usage

Run the agent from the command line:
uv run main.py "your prompt here" --verbose

Examples

List the contents of the root directory:
uv run main.py "what files are in the root?" --verbose

Read a file:
uv run main.py "get the contents of lorem.txt" --verbose

Write to a file:
uv run main.py "create a new README.md file with the contents '# calculator'" --verbose

Execute a Python file:
uv run main.py "run tests.py" --verbose

Perform a web search:
uv run main.py "search for AI agent tutorials" --verbose

How It Works
Prompt Interpretation: The user prompt is sent to the LLM.

Function Planning: The LLM decides which tool/function to call (e.g., get_files_info, write_file, run_python_file, web_search).

Function Execution: The agent calls the corresponding Python function safely, within the restricted working directory.

Feedback Loop: Results of function calls are appended to the conversation and sent back to the LLM, allowing iterative decision-making.

Completion: Once the LLM produces a text response without a function call, the agent outputs the final result.

User Prompt
     │
     ▼
+-------------------+
|   LLM Model       |
| (Function Planner)|
+-------------------+
     │
     ▼
Function Call? ──► Yes ──► Call Function (Python Tool)
     │                        │
     │                        ▼
     │                  Function Result
     │                        │
     ◄────────────────────────┘
No   │
     ▼
Final Text Response
Security Considerations
All file and Python execution operations are restricted to a specified working directory.

The agent can execute arbitrary Python code; do not use it on sensitive systems or files.

Web search results are processed as plain text and do not directly access live data outside the agent’s capabilities.

License
This project is licensed under the MIT License.
