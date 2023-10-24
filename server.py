from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from PIL import Image
import io
import os
import base64

def process_image(image_data, option, angle=None, width=None, height=None):
    try:
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        print(f"\nOperation received: {option} to manipulate the image.")
        print(width + height)

        if option == '1':
            image = image.convert('L')
        elif option == '2':
            if angle is not None:
                image = image.rotate(angle)
        elif option == '3':
            if width is not None and height is not None:
                new_width = int(image.width * width / 100)
                new_height = int(image.height * height / 100)
                image = image.resize((new_width, new_height))

        with io.BytesIO() as output:
            image.save(output, format="JPEG")
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')

        print(f"\nOperation {option} concluded. Sending the image to the client.")

        return processed_image_data
    except Exception as e:
        print(f"\nError during image manipulation: {e}")
        return ""

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def run_server():
    os.system("cls")
    host = 'localhost'
    port = 8000

    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True)

    server.register_function(process_image, 'process_image')

    print(f"\nRPC Server has been initialized & awaiting connections {host}:{port}...")
    server.serve_forever()

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nRPC server has been shut down.")
