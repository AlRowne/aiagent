import os

MAX_CHARS = 10000


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        is_valid_file_path = (
            os.path.commonpath([working_dir_abs_path, file_abs_path])
            == working_dir_abs_path
        )
        if not is_valid_file_path:
            return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_abs_path, "r") as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return contents
    except Exception as e:
        return f"Error: {e}"
