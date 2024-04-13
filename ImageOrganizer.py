import os
from datetime import datetime
from PIL import Image, UnidentifiedImageError
import shutil


def get_date_taken(file_path):
    try:
        with Image.open(file_path) as img:
            info = img._getexif()
            if 36867 in info:  # Check if "Date Taken" field is present
                date_taken = info[36867]
                return datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
    except (AttributeError, KeyError, IndexError, ValueError, UnidentifiedImageError):
        pass
    return None

def organize_photos(source_folder, destination_folder):
    # Iterate through all files in the source folder
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)

        # Get the date taken of the file
        date_taken = get_date_taken(source_path)

        if date_taken:
            # Create year and month folders in the destination folder
            year_folder = os.path.join(destination_folder, str(date_taken.year))
            month_folder = os.path.join(year_folder, f'{date_taken.month:02d}')

            os.makedirs(month_folder, exist_ok=True)

            # Copy the file to the appropriate month folder
            destination_path = os.path.join(month_folder, filename)

            # Check if the file already exists in the destination folder
            # if not os.path.exists(destination_path):
            #     # Copy the file to the appropriate month folder
            #     shutil.copy(source_path, destination_path)
            # else:
            #     print(f"File {filename} already exists in the destination folder. Skipping.")

            # Check if the file already exists in the destination folder
            counter = 1
            while os.path.exists(destination_path):
                # If file exists, append a counter to the filename
                new_filename = f"{os.path.splitext(filename)[0]}_{counter}{os.path.splitext(filename)[1]}"
                destination_path = os.path.join(month_folder, new_filename)
                counter += 1

            shutil.move(source_path, destination_path)
            print("moved file: " + source_path + " to destination: " + destination_path)

        # Move the file to the appropriate month folder
        #destination_path = os.path.join(month_folder, filename)
        #shutil.move(source_path, destination_path)

if __name__ == "__main__":
    source_folder = r"C:\Users\dobne\Pictures\ToOrganize"
    destination_folder = r"C:\Users\dobne\Pictures\Photos"

    organize_photos(source_folder, destination_folder)


# Insert folder path in runtime instead:
# def main():
#     source_folder = input("Enter the path to the source folder: ")
#
#     destination_folder = input("Enter the path to the destination folder: ")
#
#     organize_photos(source_folder, destination_folder)
#
# if __name__ == "__main__":
#     main()