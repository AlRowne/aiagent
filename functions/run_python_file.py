import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        is_valid_file_path = (
            os.path.commonpath([working_dir_abs_path, file_abs_path])
            == working_dir_abs_path
        )
        if not is_valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_abs_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_abs_path]
        if args:
            command.extend(args)

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=working_dir_abs_path,
            timeout=30,
        )
        return_string = ""
        if process.returncode != 0:
            return_string += f"Process exited with code {process.returncode}\n"
        if not process.stdout and not process.stderr:
            return_string += "No output produced\n"
        else:
            return_string += f"STDOUT: {process.stdout}\n"
            return_string += f"STDERR: {process.stderr}\n"
        return return_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
