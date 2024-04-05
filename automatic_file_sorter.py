import os


def sort_files_by_extension(source_dir, target_dir):
    # Create target directories if they don't exist
    os.makedirs(target_dir, exist_ok=True)

    # Get the list of files in the source directory
    files = os.listdir(source_dir)

    # Initialize counter for files moved
    files_moved_count = 0

    # Iterate through each file and move it to the corresponding folder based on extension
    for file_name in files:
        # Get the file extension
        _, file_extension = os.path.splitext(file_name)
        # Remove the dot from the extension and normalize folder name with lowercase characters
        file_extension = file_extension.lower()[1:]

        # Create target subdirectory if it doesn't exist
        target_subdir = os.path.join(target_dir, file_extension)
        os.makedirs(target_subdir, exist_ok=True)

        # Move the file to the target subdirectory
        source_file_path = os.path.join(source_dir, file_name)
        target_file_path = os.path.join(target_subdir, file_name)
        try:
            os.rename(source_file_path, target_file_path)
            files_moved_count += 1
            print(f"Moved {file_name} to {target_subdir}")
        except OSError as e:
            print(f"Error moving {file_name}: {e}")

    # Display success message with the count of files moved
    print(f"Successfully moved {files_moved_count} files.")


# Example usage:
if __name__ == '__main__':
    source_directory = "/path/to/source/directory"
    target_directory = "/path/to/target/directory"
    sort_files_by_extension(source_directory, target_directory)
