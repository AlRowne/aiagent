import os


def resolve_and_validate_path(
    working_dir: str, target: str
) -> tuple[str | None, str | None]:
    working_dir_abs_path = os.path.abspath(working_dir)
    target_abs_path = os.path.normpath(os.path.join(working_dir_abs_path, target))

    is_valid_target = (
        os.path.commonpath([working_dir_abs_path, target_abs_path])
    ) == working_dir_abs_path

    if not is_valid_target:
        return (
            None,
            f'Error: Cannot access "{target}" as it is outside the permitted working directory',
        )

    return target_abs_path, None
