import cv2
import numpy as np
from tkinter import Tk, filedialog, messagebox, simpledialog
import os

def crop_to_square(image_path, output_path="cropped_image.jpg"):
    """
    Crop an image to a 1:1 aspect ratio by centering the crop.
    :param image_path: Path to the input image.
    :param output_path: Path to save the cropped image.
    """
    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Unable to read the image. Please check the file path.")
        
        # Get dimensions
        height, width = image.shape[:2]
        
        # Determine the size of the square
        square_size = min(height, width)
        
        # Calculate the cropping region
        start_x = (width - square_size) // 2
        start_y = (height - square_size) // 2
        
        # Crop the image
        cropped_image = image[start_y:start_y + square_size, start_x:start_x + square_size]
        
        # Save the cropped image
        cv2.imwrite(output_path, cropped_image)
        print(f"Image successfully cropped and saved at {output_path}")
    except Exception as e:
        print(f"Error: {e}")

def crop_to_aspect_ratio(image, aspect_ratio):
    """
    Crop an image to a specified aspect ratio (3:2).
    :param image: Input image array.
    :param aspect_ratio: Desired aspect ratio as a tuple (width, height).
    :return: Cropped image.
    """
    height, width = image.shape[:2]
    
    if aspect_ratio == (3, 2):
        target_width = width
        target_height = int(width * 2 / 3)  # Calculate height based on width for 3:2

        if target_height > height:
            target_height = height
            target_width = int(height * 3 / 2)  # Adjust width based on height for 3:2

    else:
        return None

    start_x = (width - target_width) // 2
    start_y = (height - target_height) // 2
    
    return image[start_y:start_y + target_height, start_x:start_x + target_width]

def select_and_crop_image():
    """
    GUI-based method to select an image and crop it.
    """
    root = Tk()
    root.withdraw()  # Hide the main window

    try:
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
        )
        if not file_path:
            messagebox.showinfo("Info", "No file selected.")
            return

        # Ask user for cropping option
        crop_option = simpledialog.askstring("Crop Option", "Enter '1' for 1:1 or '2' for 3:2:")
        
        if crop_option not in ['1', '2']:
            messagebox.showerror("Error", "Invalid option selected. Please enter '1' or '2'.")
            return
        
        # Generate output file path
        base_name = os.path.basename(file_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(os.path.dirname(file_path), f"{name}_cropped{ext}")

        # Read the image
        image = cv2.imread(file_path)

        if crop_option == '1':
            crop_to_square(file_path, output_path)
        
        elif crop_option == '2':
            cropped_image = crop_to_aspect_ratio(image, (3, 2))
            if cropped_image is not None:
                cv2.imwrite(output_path, cropped_image)
                print(f"Image successfully cropped to 3:2 and saved at {output_path}")
            else:
                messagebox.showerror("Error", "Could not crop the image to 3:2 aspect ratio.")

        # Notify user
        messagebox.showinfo("Success", f"Cropped image saved at: {output_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    select_and_crop_image()
