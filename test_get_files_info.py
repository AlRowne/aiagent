from functions.get_files_info import get_files_info


def print_files_info(working_dir: str, directory: str):
    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    if get_files_info(working_dir, directory).startswith("Error"):
        print(f"{get_files_info(working_dir, directory)}")
    else:
        print(f"{get_files_info(working_dir, directory)}")


print_files_info("calculator", ".")
print_files_info("calculator", "pkg")
print_files_info("calculator", "/bin")
print_files_info("calculator", "../")
