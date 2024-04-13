import datetime
import os
import shutil
import time

import schedule


def create_backup_folder(destination_path):
    """
    Creates a new folder in the specified destination directory.

    Args:
        destination_path (str): The base directory for backups.

    Returns:
        str: The full path to the newly created folder.
    """
    today = datetime.date.today().isoformat()  # Get today's date in ISO format
    new_folder = os.path.join(destination_path, today)
    try:
        os.makedirs(
            new_folder, exist_ok=True
        )  # Use exist_ok=True to avoid FileExistsError
        return new_folder
    except FileExistsError:
        print(f"Backup folder already exists: {new_folder}")
        return new_folder  # Return existing folder path to continue copying


def copy_folder_to_directory(source_path, destination_path):
    """
    Copies the contents of the source folder to the destination directory.

    Args:
        source_path (str): The path to the source folder containing files to copy.
        destination_path (str): The path to the destination directory for the backup.
    """
    dest_dir = create_backup_folder(destination_path)

    try:
        shutil.copytree(source_path, dest_dir, dirs_exist_ok=True)
        print(f"Folder copied to: {dest_dir}")
    except Exception as e:
        print(f"Error copying folder: {e}")


if __name__ == "__main__":
    # Define source and destination directory paths (modify as needed)
    source_path = "/path/to/source/folder"
    destination_path = "/path/to/destination/folder"

    # Schedule daily backup at 18:00
    schedule.every().day.at("18:00").do(
        lambda: copy_folder_to_directory(source_path, destination_path)
    )

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check for pending tasks every minute
