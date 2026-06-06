import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        is_valid_file_path = (
            os.path.commonpath([working_dir_abs_path, file_abs_path])
            == working_dir_abs_path
        )
        if not is_valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(file_abs_path), exist_ok=True)
        with open(file_abs_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
