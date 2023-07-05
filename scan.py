import os
import sane
import random
from datetime import datetime
from PIL import Image
from metadata_extraction import MetadataExtractor

target_folder = 'scannedImages' # folder where scanned images along with their metadata will be stored.
test_images_folder = 'testImages'  # folder containing the test images for test scans.


def get_folder_path(target_folder):
    """Returns the path of a new folder to be created in the target folder."""
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_folder_name = f"Image_{timestamp}"
    folder_path = os.path.join(target_folder, new_folder_name)
    return folder_path


def ask_for_test_mode():
    """Asks the user if they want to run in test mode and returns the response."""
    
    response = input("Would you like to run in test mode? (yes/no): ")
    return response.lower() == 'yes'


def scan_and_store_document(target_folder, test_image_path, test_mode=False):
    """ Scans and stores a document in the target folder.If a scanner is not available or test_mode is True, uses a test image."""
   
    # Creating a folder for storing the image and it's metadata
    folder_path = get_folder_path(target_folder)
    os.makedirs(folder_path, exist_ok=True)

    sane.init()
    devices = sane.get_devices()

    if not devices:
        if not test_mode:
            print("No scanner found. Switching to test mode.")
        test_mode = True

    if not test_mode:
        # Display available scanners to the user
        print("Available Scanners:")
        for i, device in enumerate(devices):
            print(f"{i + 1}. {device[1]}")

        # Prompt the user to select a scanner
        scanner_index = input("Enter the index of the scanner you want to use: ")
        try:
            scanner_index = int(scanner_index) - 1
            if scanner_index < 0 or scanner_index >= len(devices):
                print("Invalid scanner index.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        scanner = sane.open(devices[scanner_index][0])
        print(f"Selected scanner: {devices[scanner_index][1]}")
    else:
        print("Test mode activated. Using test image instead of scanning.")

    try:
        if not test_mode:
            scanner.resolution = 300
            scanner.start()
            scanned_image = scanner.snap()  # Obtain the scanned image
        else:
            scanned_image = Image.open(test_image_path)  # Use the test image

        # If the image has an alpha channel or is in mode 'P', convert it to RGB
        if scanned_image.mode in ['RGBA', 'P']:
            scanned_image = scanned_image.convert('RGBA').convert('RGB')

        # Save the scanned image
        filename = "image.jpg"
        image_path = os.path.join(folder_path, filename)
        scanned_image.save(image_path, 'JPEG')
        print(f"Scanned image saved as {filename}")

        # Save the metadata
        extractor = MetadataExtractor()
        metadata = extractor.extract_metadata(str(image_path))
        output_metadata = "\n".join([f"{key}: {metadata[key]}" for key in metadata])
        metadata_filename = "metadata.txt"
        metadata_path = os.path.join(folder_path, metadata_filename)
        with open(metadata_path, 'w') as metadata_file:
            metadata_file.write(output_metadata)
        print(f"Metadata saved as {metadata_filename}")

    except Exception as e:
        print(f"An error occurred during scanning: {e}")

    finally:
        # Close the scanner
        if not test_mode:
            scanner.close()
        sane.exit()


test_mode = ask_for_test_mode()

# Get a list of all files in the directory for test mode
test_images = os.listdir(test_images_folder)

# Select a random image from the directory for testing if test-mode is true or if no scanners were found
test_image_path = os.path.join(test_images_folder, random.choice(test_images))

scan_and_store_document(target_folder, test_image_path, test_mode=test_mode)
