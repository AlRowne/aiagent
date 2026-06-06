import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, creating it or overwriting it if it already exists",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            ),
        },
    ),
)


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
