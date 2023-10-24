import xmlrpc.client
import os
import base64
import tkinter as tk
from tkinter import filedialog

url = "http://localhost:8000"
server = xmlrpc.client.ServerProxy(url, allow_none=True)

def send_image_and_option(image_path, option, angle, width, height):
    try:
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        if option == '1':
            processed_image_data = server.convert_to_grayscale(image_data)
        elif option == '2':
            if angle is not None:
                processed_image_data = server.rotate_image(image_data, angle)
        elif option == '3':
            if width is not None and height is not None:
                processed_image_data = server.resize_image(image_data, width, height)
        elif option == '4':
            processed_image_data = server.apply_blur(image_data)

        if processed_image_data is not None:
            with open('processed_image.jpg', 'wb') as processed_image_file:
                processed_image_file.write(base64.b64decode(processed_image_data))

            print("\nImage has been successfully manipulated & saved as 'processed_image.jpg'.")
    except Exception as e:
        print(f"Error {e}")

def select_image():
    os.system("cls")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    return file_path

if __name__ == "__main__":
    image_path = None

    while True:
        if image_path is None:
            print("No image selected.")
            image_path = select_image()

        print("\n0 - Select another image")
        print("1 - Convert to Grayscale")
        print("2 - Rotate Image")
        print("3 - Resize Image")
        print("4 - Apply Blur")
        print("5 - Disconnect")

        option = input("Choose an option: ").strip()
        os.system("cls")

        if option == '0':
            image_path = select_image()
            continue
            
        elif option == '1' and image_path:
            send_image_and_option(image_path, option, None, None, None)

        elif option == '2' and image_path:
            angle = input("\nEnter the angle for rotation (in degrees): ")
            os.system("cls")
            if not angle:
                print("\nNo angle provided. Skipping rotation.")
            else:
                send_image_and_option(image_path, option, int(angle), None, None)

        elif option == '3' and image_path:
            width = float(input("\nEnter the width resize in pxs (e.g: 140): "))
            height = float(input("\nEnter the height resize in pxs (e.g: 140): "))
            os.system("cls")
            if width and height:
                send_image_and_option(image_path, option, None, width, height)
            else:
                print("\nInvalid resize percentage. Skipping resize.")

        elif option == '4' and image_path:
            send_image_and_option(image_path, option, None, None, None)

        elif option == '5':
            leave = input("\nAre you sure you want to disconnect the server (y/n):").lower()
            if leave == 'y':
                os.system("cls")
                print("\nLeaving the server...\n")
                break
            else:
                os.system("cls")
        else:
            print("\nInvalid Option, Try Again.")
