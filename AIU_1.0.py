import os
import zipfile
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from threading import Thread
import datetime
import traceback

version=str(1.0)
file_types = {
        '3D_objects': ['.fbx', '.dae', '.blend' ], 
        # '.3ds' works but requires minor changes (no "textures" folder, only .jpg, but texture is built into .3ds file)
        # Didn't work in unity: '.obj', '.stl', '.ply', '.wrl' 
        # Requires further testing:'.dxf'
        # .blend works seemlessly but can also be used for materials
        
        #'WIP': ['.3ds', '.hdr', '.exr', '.glTF', '.glb', '.blend'],
        #'HDRIs': ['.hdr', '.exr'],
        #'Materials': [] # Consider identifying all .gltf files as Materials? (Otherwise Materials won't be available at all)
        #'Unclear': ['.glTF', '.glb', '.blend'], # These files can be either 3D objects or Materials
        #'Unsupported': ['.usd', '.usdc', '.usda'] # USD not supported in Unity?
    }


def extract_zip(zip_path, extract_path):
    # Extract zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def read_and_rename(filename, textures_folder_path):
    # Extract relevant information from the filename
    #prefix = fbx_filename.split('_1k')[0] # /// Temporary solution, needs to be updated later
    prefix, _ = os.path.splitext(filename) # Updated solution
    new_folder_name = f"{prefix}_txtr"

    # Check if the textures folder exists before renaming
    if os.path.exists(textures_folder_path):
        # Rename the textures folder
        os.rename(textures_folder_path, os.path.join(os.path.dirname(textures_folder_path), new_folder_name))

def process_3d_objects(file_path, textures_path, imported_assets_path):
    #print('3D objects')
    # Find the object file and textures folder
    for root, dirs, files in os.walk(file_path):
        for file in files:
            #if file.endswith(".fbx"):
            file_extension = os.path.splitext(file)[1] #///
            if file_extension in file_types['3D_objects']: #///
                filename = file
                textures_folder_path = os.path.join(root, "textures")

                # Call Function: Process and rename the textures folder
                read_and_rename(filename, textures_folder_path)
    
    # Move object file to the 'Imported Assets' folder
    for root, dirs, files in os.walk(file_path):
        for file in files:
            #if file.endswith(".fbx"):
            file_extension = os.path.splitext(file)[1] #///
            if file_extension in file_types['3D_objects']: #///
                fbx_path = os.path.join(root, file)
                destination_path = os.path.join(imported_assets_path, file)

                # Check if the file with the same name already exists in the destination
                if not os.path.exists(destination_path):
                    #print(f"Moving .fbx file: {fbx_path} -> {destination_path}")
                    shutil.move(fbx_path, destination_path)
                else:
                    print(f"File already exists in destination: {destination_path}")
            #else: 
                # Frequent false positives
                #print(f"Ignoring file: {file}")

    # Move renamed textures folder to the 'Textures' folder          
    for root, dirs, files in os.walk(file_path):
        for directory in dirs:
            if directory.endswith("_txtr"):
                source_path = os.path.join(root, directory)
                destination_path = os.path.join(textures_path, directory)

                # Check if the directory with the same name already exists in the destination
                if not os.path.exists(destination_path):
                    #print(f"Moving directory: {source_path} -> {destination_path}")
                    shutil.move(source_path, destination_path)
                else:
                    print(f"Directory already exists in destination: {destination_path}")
            #else:
                # Frequent false positives
                #print(f"Ignoring file: {file}")

def process_unrecognized(file_path, forced):
    print('Unrecognized')
    pass

def sort_files(file_path, unity_project_path, textures_path, imported_assets_path):
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # Determine the type of the file based on its extension
    for key, extensions in file_types.items():
        if file_extension.lower() in extensions:
            # Delegate to the corresponding processing function
            processing_function = globals().get(f"process_{key.lower()}", None)
            if processing_function:
                processing_function(file_path, textures_path, imported_assets_path)
            else:
                print(f"Warning: No processing function defined for file type '{key}'.")
            break
    ''' // Force unstable
    else: #/// force feature untested
        # If no matching file type is found, prompt the user to force a specific function
        force_process = input(f"One or more file types are unrecognized or have not yet been implemented. Do you want to force processing? (y/n): ").lower()
        if force_process == 'y': # /// needs ui transfer
            force_function = input("Enter the function to force processing (e.g., '3d_objects', 'hdris'): ").lower()
            processing_function = globals().get(f"process_{force_function}", process_unrecognized)
            forced = (True)
            processing_function(file_path, forced)
        else:
            print("File processing skipped.")
    '''

def process_file(zip_directory, unity_project_path, progress_var, is_running_var):
    try:
        is_running_var.set(True)
        forced = (False)
        # Identify zipfolders
        # Currently it ignores unzipped folders, can leave this as an option and then add a "include unzipped folders" toggle
        zip_files = [f for f in os.listdir(zip_directory) if f.endswith(".zip")]

        if not zip_files:
            result_label.config(text="No zip files found in the specified directory.")
            return

        total_zips = len(zip_files)
        current_zip = 0

        
        for zip_file in zip_files:
            current_zip += 1
            progress_percentage = int((current_zip / total_zips) * 100)
            progress_var.set(progress_percentage)

            zip_path = os.path.join(zip_directory, zip_file)

            # Create a unique extraction directory based on the zip file name
            extract_path = os.path.join(zip_directory, f"temp_extraction_{zip_file[:-4]}")

            # Check if the extraction directory already exists and remove its contents
            if os.path.exists(extract_path):
                shutil.rmtree(extract_path)

            # Call Function: Extract the contents of the zip file
            extract_zip(zip_path, extract_path)

            # Call Function: create import folders and return path
            textures_path, imported_assets_path = setup_unity_import(unity_project_path)

            # Call Function: sort files by file type/extension
            sort_files(extract_path, unity_project_path, textures_path, imported_assets_path)

            # Call Function: Import to unity
            #move_files_to_unity_project(extract_path, unity_project_path)
         
            # Cleanup: Remove the temp_extraction folder after moving its contents
            shutil.rmtree(extract_path)

            # Cleanup: Delete only the zip file after processing
            os.remove(zip_path)

        result_label.config(text="Script executed successfully.")

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")
        
        # Create a debug log file with timestamp
        log_filename = f"debug_log_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        log_path = os.path.join(zip_directory, log_filename)
        with open(log_path, 'w') as log_file:
            log_file.write(f"\nVersion_{version}\nError: {str(e)}")
            traceback.print_exc(file=log_file)

    finally:
        is_running_var.set(False)

def setup_unity_import(unity_project_path):
    # Create 'Imported Assets' folder within the 'Assets' folder of the Unity project
    imported_assets_path = os.path.join(unity_project_path, "Assets", "Imported Assets")
    os.makedirs(imported_assets_path, exist_ok=True)

    # Create 'Textures' folder within the 'Imported Assets' folder
    textures_path = os.path.join(imported_assets_path, "Textures")
    os.makedirs(textures_path, exist_ok=True)
    return textures_path, imported_assets_path


# Define UI buttons
def browse_button():
    folder_selected = filedialog.askdirectory()
    entry_path.delete(0, tk.END)
    entry_path.insert(0, folder_selected)
    result_label.config(text="")

def browse_unity_project_button():
    folder_selected = filedialog.askdirectory()
    entry_unity_path.delete(0, tk.END)
    entry_unity_path.insert(0, folder_selected)
    result_label.config(text="")

def run_button():
    if is_running_var.get():
        result_label.config(text="Error: Script is already running.")
    else:
        zip_directory = entry_path.get()
        unity_project_path = entry_unity_path.get()
        if os.path.exists(zip_directory) and os.path.exists(unity_project_path):
            progress_var.set(0)  # Reset progress bar
            Thread(target=process_file, args=(zip_directory, unity_project_path, progress_var, is_running_var)).start()
        else:
            result_label.config(text="Error: Invalid directory paths.")

# Create the main window
root = tk.Tk()
root.title("File Renaming Script")

# Create and place GUI elements
label_guide = tk.Label(root, text="Instructions:\n1. Click 'Browse' to select the folder containing your zip files.\n2. Click 'Browse Unity Project' to select the Unity project folder.\n3. Click 'Run Script' to execute the file renaming script.")
label_guide.pack()

label_path = tk.Label(root, text="Enter the path to the zip files:")
label_path.pack()

entry_path = tk.Entry(root, width=50)
entry_path.pack()

browse_button = tk.Button(root, text="Browse", command=browse_button)
browse_button.pack()

label_unity_path = tk.Label(root, text="Enter the path to the Unity project:")
label_unity_path.pack()

entry_unity_path = tk.Entry(root, width=50)
entry_unity_path.pack()

browse_unity_project_button = tk.Button(root, text="Browse Unity Project", command=browse_unity_project_button)
browse_unity_project_button.pack()

run_button = tk.Button(root, text="Run Script", command=run_button)
run_button.pack()

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, length=200, mode='determinate')
progress_bar.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Variable to track whether the script is currently running
is_running_var = tk.BooleanVar()
is_running_var.set(False)

# Start the GUI event loop
root.mainloop()
