import os
import shutil

source_dir = r"D:\Tsunami Modeling\Kamchatka M8.8 2025\unit_sources"
target_dir = r"D:\Tsunami Modeling\Kamchatka M8.8 2025\comcot_run"
base_files_dir = r"D:\Tsunami Modeling\Kamchatka M8.8 2025\comcot_base"


for filename in os.listdir(source_dir):
    if filename.endswith(".txt"):
        folder_name = os.path.splitext(filename)[0]
        folder_path = os.path.join(target_dir, folder_name)

        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")

        for base_file in os.listdir(base_files_dir):
            src_file = os.path.join(base_files_dir, base_file)
            dst_file = os.path.join(folder_path, base_file)
            shutil.copy2(src_file, dst_file)

        print(f"Copied base files to: {folder_path}")

        for folder_name in os.listdir(target_dir):
            folder_path = os.path.join(target_dir, folder_name)

            if os.path.isdir(folder_path):
                ctl_path = os.path.join(folder_path, "comcot.ctl")

            if os.path.isfile(ctl_path):
                with open(ctl_path, 'r') as f:
                    lines = f.readlines()

            if len(lines) >= 40:
                # modify file name input data inside comcot.ctl with source .txt files
                modified_line = lines[39][:50] + "../../unit_sources/" + folder_name + ".txt\n"
                lines[39] = modified_line

                # Overwrite the file with the updated content
                with open(ctl_path, 'w') as f:
                    f.writelines(lines)
                
        print(f"Source file assigned to: {folder_path}")

