from pathlib import Path


def resolve_filename(directory, filename, extension):
    output_path = Path(directory) / f"{filename}.{extension}"

    if not output_path.exists():
        return filename

    return None


def generate_unique_filename(directory, filename, extension):
    counter = 1

    while True:
        new_name = f"{filename}_{counter}"
        output_path = Path(directory) / f"{new_name}.{extension}"

        if not output_path.exists():
            return new_name

        counter += 1