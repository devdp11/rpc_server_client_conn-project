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

        if option == '2':
            image = image.convert('L')
        elif option == '3':
            if angle is not None:
                image = image.rotate(angle)
        elif option == '4':
            if width is not None and height is not None:
                image = image.resize((width, height))

        with io.BytesIO() as output:
            image.save(output, format="JPEG")
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')

        print(f"\nOperation {option} concluded. Sending the image to the client.")

        return processed_image_data
    except Exception as e:
        print(f"Error during image manipulation: {e}")
        return ""

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def run_server():
    os.system("cls")
    host = 'localhost'
    port = 8000

    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler)

    server.register_function(process_image, 'process_image')

    print(f"\nRPC Server has been initialized & awaiting connections {host}:{port}...")
    server.serve_forever()

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nRPC server has been shut down.")
