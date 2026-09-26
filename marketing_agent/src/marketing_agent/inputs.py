from pathlib import Path

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def select_newest_unprocessed_input_folder(root: Path):
    # A marker advances the next run without deleting the user's input files.
    folders = (
        [
            path
            for path in root.iterdir()
            if path.is_dir() and not (path / ".processed").exists()
        ]
        if root.is_dir()
        else []
    )
    if not folders:
        raise FileNotFoundError(f"No unprocessed input folder found in: {root}")

    folder = max(folders, key=lambda path: path.stat().st_ctime)
    query_files = [
        path
        for path in folder.iterdir()
        if path.is_file()
        and path.stem.lower().endswith("_query")
        and path.suffix.lower() in {".md", ".txt"}
    ]
    if len(query_files) != 1:
        raise ValueError(
            f"Input folder requires exactly one *_query.md or *_query.txt file: {folder}"
        )
    query_file = query_files[0]

    source_paths = [
        str(path)
        for path in folder.iterdir()
        if path.is_file()
        and path != query_file
        and path.suffix.lower() in {".md", ".txt"}
    ]
    image_paths = [
        str(path)
        for path in folder.iterdir()
        if path.is_file()
        and path.stem.lower().endswith("_image")
        and path.suffix.lower() in IMAGE_SUFFIXES
    ]
    return (
        folder,
        query_file.read_text(encoding="utf-8").strip(),
        source_paths,
        image_paths,
    )
