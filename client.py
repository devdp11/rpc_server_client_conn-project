import xmlrpc.client
import os
import base64
import tkinter as tk
from tkinter import filedialog
import sys

url = "http://localhost:8000"
server = xmlrpc.client.ServerProxy(url, allow_none=True)

def send_image_and_option(image_path, option, angle, width, height):
    try:
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        if option == '1':
            processed_image_data = server.convert_image(image_data)
            image_operation = 'grayscale'
        elif option == '2':
            if angle is not None:
                processed_image_data = server.rotate_image(image_data, angle)
                image_operation = 'rotate'
        elif option == '3':
            if width is not None and height is not None:
                processed_image_data = server.resize_image(image_data, width, height)
                image_operation = 'resize'
        elif option == '4':
            processed_image_data = server.blur_image(image_data)
            image_operation = 'blur'

        if processed_image_data is not None:
            with open(f'{os.path.splitext(image_path)[0]}_{image_operation}.jpg', 'wb') as processed_image_file:
                processed_image_file.write(base64.b64decode(processed_image_data))

            print(f"\nImage has been successfully manipulated & saved as '{os.path.splitext(os.path.basename(image_path))[0]}_{image_operation}.jpg'.")
    except Exception as e:
        print(f"Error {e}")

def select_image():
    os.system("cls")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    return file_path if file_path else None

if __name__ == "__main__":
    while True:
        image_path = None

        if image_path is None:
            image_path = select_image()
        
        if image_path is not None:
            while True:
                print("\n0 - Select another image")
                print("1 - Convert to Grayscale")
                print("2 - Rotate Image")
                print("3 - Resize Image")
                print("4 - Apply Blur")
                print("5 - Disconnect")

                option = input("Choose an option: ").strip()
                os.system("cls")

                if option == '0':
                    image_path = None
                    if image_path is None:
                        while True:
                            image_path = select_image()
                            if image_path is not None:
                                break


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
                    width = int(input("\nEnter the width resize in pxs (e.g: 140): "))
                    height = int(input("\nEnter the height resize in pxs (e.g: 140): "))
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
                        sys.exit(1)
                    else:
                        os.system("cls")
                else:
                    print("\nSelect Image or a valid option.")
