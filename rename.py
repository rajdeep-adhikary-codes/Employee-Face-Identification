import os
import uuid
import shutil

counter = 0

def rename_files(folder_path, new_name):
    global counter  # Declare counter as global
    
    # Get list of files in the folder
    files = os.listdir(folder_path)
    
    # Iterate through each file
    for filename in files:
        # Split the filename and extension
        name, extension = os.path.splitext(filename)
        
        # Generate a unique identifier
        unique_id = new_name + '_' + str(counter)
        
        # Create the new filename with unique id and original extension
        new_filename = unique_id + extension
        
        # Construct the full paths of old and new filenames
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_file_path, new_file_path)
        
        counter += 1
        
        print(f"Renamed '{filename}' to '{new_filename}'")

def rename_folders(folder_path):
    # Get list of files in the folder
    original_folder = folder_path
    folder_path = folder_path + '/train/'
    folders = os.listdir(folder_path)

    for folder in folders:

        if os.path.isdir(folder_path + folder):

            new_folder_name = uuid.uuid4().hex

            # Construct the full paths of old and new filenames
            old_folder_path = os.path.join(folder_path, folder)
            new_folder_path = os.path.join(folder_path, new_folder_name)

            # Rename the file
            os.rename(old_folder_path, new_folder_path)

            print(f"Renamed folder - '{folder}' to '{new_folder_name}")

            rename_files(new_folder_path, new_folder_name)

            change_specific_filename(folder, new_folder_name, original_folder + '/test/')
            

def move_to_root(folder_path):
    folders = os.listdir(folder_path)
    for folder in folders:
        if os.path.isdir(folder_path + folder):
            files = os.listdir(folder_path + folder)
            for file in files:
                shutil.move(folder_path + folder + '/' + file, folder_path + file)
                print(f"moved {file}")
            os.rmdir(folder_path + folder)
            print(f"Deleted {folder_path + folder}")

def change_specific_filename(filename, new_filename, directory):
    files = os.listdir(directory)
    for file in files:
        if file.startswith(filename):
            name, extension = os.path.splitext(file)
            old_file_path = os.path.join(directory, file)
            new_file_path = os.path.join(directory, new_filename + extension)

            os.rename(old_file_path, new_file_path)

            print(f"changed test file '{file}' to '{new_filename + extension}'");

            return
        

# Example usage
folder_path = './dataset'
# rename_folders(folder_path)
folder_path += '/train/'
move_to_root(folder_path)
