# AI Agent

A CLI coding agent powered by Google Gemini that can autonomously read, write, and execute files within a working directory.

## How it works

The agent takes a natural-language prompt, builds a function-call plan, and iteratively calls tools until it produces a final answer. Each iteration feeds tool results back into the model (up to 20 rounds).

### Available tools

| Tool | Description |
|---|---|
| `get_files_info` | List files and directories |
| `get_file_content` | Read the contents of a file |
| `write_file` | Write or overwrite a file |
| `run_python_file` | Execute a Python file with optional arguments |

All tool calls are sandboxed to a working directory (`./calculator` by default).

## Setup

**Prerequisites:** Python 3.13+, [uv](https://github.com/astral-sh/uv)

```bash
uv sync
```

Create a `.env` file with your Gemini API key:

```
GEMINI_API_KEY=your_key_here
```

## Usage

```bash
uv run main.py "your prompt here"
uv run main.py "your prompt here" --verbose
```

`--verbose` prints token counts and full function call arguments.

### Example

```bash
uv run main.py "How many tests are passing in the calculator module?"
```

## Project structure

```
main.py               # Entry point and agent loop
prompts.py            # System prompt
functions/
  call_function.py    # Dispatches function calls from the model
  get_files_info.py   # Tool: list files
  get_file_content.py # Tool: read file
  write_file.py       # Tool: write file
  run_python_file.py  # Tool: run Python
  _path_utils.py      # Path validation helpers
calculator/           # Sample working directory the agent operates on
```
