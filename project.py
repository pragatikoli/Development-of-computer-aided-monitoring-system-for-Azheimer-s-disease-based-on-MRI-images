import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
from PIL import Image, ImageFilter
import cv2
import numpy as np

# Sample username and password
USERNAME = "admin"
PASSWORD = "12"

# Sample dataset directory
DATASET_DIR = r"C:\Users\praga\Downloads\archive"

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == USERNAME and password == PASSWORD:
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        open_next_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_next_page():
    root.withdraw()  # Hide the login window
    next_page_window = tk.Toplevel(root)
    next_page_window.title("Upload images")
    next_page_window.geometry("800x500")

    # Function to display information about Alzheimer's disease
    def show_alzheimer_info():
        messagebox.showinfo("Alzheimer's Information",
                            "Alzheimer's disease is a progressive disorder that causes brain cells to degenerate and die. It is the most common cause of dementia, a continuous decline in thinking, behavioral, and social skills that disrupts a person's ability to function independently.")

    # Button to display Alzheimer's information
    alzheimer_info_button = tk.Button(
        next_page_window, text="Alzheimer's Information", command=show_alzheimer_info)
    alzheimer_info_button.pack(pady=10)

    # Button to close the window
    close_button = tk.Button(
        next_page_window, text="Close", command=next_page_window.destroy)
    close_button.pack(pady=10)

    # Function to handle image upload, classification, and filter
    def upload_and_analyze():
        file_path1 = filedialog.askopenfilename(title="Choose Image 1")
        file_path2 = filedialog.askopenfilename(title="Choose Image 2")
        if file_path1 and file_path2:
            # Open the images
            original_image1 = Image.open(file_path1)
            original_image2 = Image.open(file_path2)

            # Apply Gaussian blur filter
            filtered_image1 = original_image1.filter(
                ImageFilter.GaussianBlur(radius=2))  # Adjust radius as needed
            filtered_image2 = original_image2.filter(
                ImageFilter.GaussianBlur(radius=2))  # Adjust radius as needed

            # Display the filtered images
            filtered_image1.show()
            filtered_image2.show()

            # Process and analyze the images using OpenCV
            progress = process_and_analyze_images(
                file_path1, file_path2, original_image1, original_image2)

            messagebox.showinfo("Analysis Result", f'Progress: {progress:.2f}%')

    # Button to upload images and apply Gaussian filter
    analyze_button = tk.Button(
        next_page_window, text="Upload and Analyze Images", command=upload_and_analyze)
    analyze_button.pack(pady=10)

def process_and_analyze_images(file_path1, file_path2, original_image1, original_image2):
    # Read the images
    img1 = cv2.imread(file_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(file_path2, cv2.IMREAD_GRAYSCALE)

    # Check if the images are loaded correctly
    if img1 is None or img2 is None:
        print("Error: Unable to load image(s).")
    else:
        # Threshold the images to create binary images
        _, binary_img1 = cv2.threshold(img1, 128, 255, cv2.THRESH_BINARY)
        _, binary_img2 = cv2.threshold(img2, 128, 255, cv2.THRESH_BINARY)

        # Display the images
        cv2.imshow('Image 1', binary_img1)
        cv2.imshow('Image 2', binary_img2)

        # Count the number of white and black pixels
        number_of_white_pix1 = np.sum(binary_img1 == 255)
        number_of_black_pix1 = np.sum(binary_img1 == 0)

        number_of_white_pix2 = np.sum(binary_img2 == 255)
        number_of_black_pix2 = np.sum(binary_img2 == 0)

        # Calculate the ratios
        Ratio1 = number_of_white_pix1 / number_of_black_pix1 if number_of_black_pix1 != 0 else float('inf')
        Ratio2 = number_of_white_pix2 / number_of_black_pix2 if number_of_black_pix2 != 0 else float('inf')

        # Calculate progress
        progress = calculate_progress(Ratio1, Ratio2)
 
        # Wait for a key press and close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return progress

def calculate_progress(Ratio1, Ratio2):
    # Calculate progress
    if Ratio1 == float('inf') or Ratio2 == float('inf'):
        return 0  # Return 0 if the division was not possible

    progress = ((Ratio2 - Ratio1) / Ratio1) * 100 if Ratio1 != 0 else 0
    return progress

# Create main window
root = tk.Tk()
root.title("Login")
root.geometry("800x500")

# Username label and entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=100, pady=90)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=100, pady=90)

# Password label and entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=100, pady=90)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=100, pady=90)

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Keep IDLE running even after Tkinter window is closed
root.protocol("WM_DELETE_WINDOW", root.iconify)

# Run the main event loop
root.mainloop()
