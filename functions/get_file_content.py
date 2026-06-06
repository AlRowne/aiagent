import os

from google.genai import types

MAX_CHARS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to read, relative to the working directory",
            ),
        },
    ),
)


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
