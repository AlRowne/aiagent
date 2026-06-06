import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))
        is_valid_target_dir = (
            os.path.commonpath([working_dir_abs_path, target_dir])
            == working_dir_abs_path
        )
        if not is_valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files = os.listdir(target_dir)
        file_infos = []

        for file in files:
            full_path = os.path.join(target_dir, file)
            file_infos.append(
                (file, os.path.getsize(full_path), os.path.isdir(full_path))
            )

        return "\n".join(
            f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            for name, size, is_dir in file_infos
        )

    except Exception as e:
        return f"Error: {e}"
