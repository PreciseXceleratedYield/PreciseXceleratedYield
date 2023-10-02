import os
import shutil
import zipfile
import datetime

# Source directory
source_dir = r'C:\laks'

# Excluded directory
excluded_dir = r'C:\laks\sys\pxy\run'

# Backup directory
backup_dir = r'C:\laks\sys\pxy\run\backup'

# Get the current date and time
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')

# Create a backup directory with the timestamp
backup_dir_with_timestamp = os.path.join(backup_dir, f'backup_{timestamp}')
os.makedirs(backup_dir_with_timestamp)

# Iterate over files and directories in the source directory
for root, dirs, files in os.walk(source_dir):
    # Check if the current directory is the excluded directory
    if root.startswith(excluded_dir):
        continue  # Skip this directory and its contents
        
    for file in files:
        file_path = os.path.join(root, file)
        
        # Calculate the relative path from the source directory to the file
        relative_path = os.path.relpath(file_path, source_dir)
        
        # Construct the destination path in the backup directory
        dest_path = os.path.join(backup_dir_with_timestamp, relative_path)
        
        # Create directories if they don't exist in the destination
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Copy the file to the backup directory
        shutil.copy2(file_path, dest_path)

# Create a zip file with the timestamp
backup_zip_file = os.path.join(backup_dir, f'backup_{timestamp}.zip')
with zipfile.ZipFile(backup_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(backup_dir_with_timestamp):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, backup_dir_with_timestamp)
            zipf.write(file_path, relative_path)

# Clean up the temporary backup directory
shutil.rmtree(backup_dir_with_timestamp)

print(f'Backup completed to {backup_zip_file}')
