import xmlrpc.client
import os
import base64
import tkinter as tk
from tkinter import filedialog

server_url = "http://localhost:8000"
server = xmlrpc.client.ServerProxy(server_url)

def send_image_and_option(image_path, option, angle=None, width=None, height=None):
    try:
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        if option == '2' and angle is not None:
            # If the option is '2' (rotate), include the angle in the request
            processed_image_data = server.process_image(image_data, option, angle)
        elif option == '3' and width is not None and height is not None:
            # If the option is '3' (resize), include width and height in the request
            processed_image_data = server.process_image(image_data, option, width, height)
        else:
            processed_image_data = server.process_image(image_data, option)

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
            print("\nNo image selected.")
            image_path = select_image()

        print("\n1 - Select another image")
        print("2 - Gray-White Image")
        print("3 - Rotate Image")
        print("4 - Resize Image")
        print("0 - Disconnect")

        option = input("Choose an option: ").strip()

        if option == '1':
            image_path = select_image()
            continue
        elif option == '2' and image_path:
            os.system("cls")
            send_image_and_option(image_path, option)
        elif option == '3':
            os.system("cls")
            angle = input("\nEnter the angle for rotation (in degrees): ")
            if not angle:
                print("\nNo angle provided. Skipping rotation.")
            else:
                os.system("cls")
                send_image_and_option(image_path, option, int(angle))
        elif option == '4' and image_path:
            os.system("cls")
            width = input("\nEnter the width: ")
            height = input("Enter the height: ")
            if not width or not height:
                print("\nInvalid dimensions. Skipping resizing.")
            else:
                os.system("cls")
                send_image_and_option(image_path, option, None, int(width), int(height))
        elif option == '0':
            os.system("cls")
            leave = input("\nAre you sure you want to disconnect the server? (y/n):").lower()
            if leave == 'y':
                os.system("cls")
                print("\nLeaving the program...")
                break
            else:
                os.system("cls")
        else:
            print("\nInvalid Option, Try Again.")
