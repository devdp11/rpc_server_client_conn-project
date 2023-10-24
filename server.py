from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from PIL import Image
import io
import base64
from PIL import ImageFilter

def convert_to_grayscale(encoded_image):
    try:
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(image_bytes))
        gray_image = image.convert('L')
        with io.BytesIO() as output:
            gray_image.save(output, format="JPEG")
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')
        return processed_image_data
    except Exception as e:
        print(f"\nError during image manipulation: {e}")
        return ""

def resize_image(encoded_image, width, height):
    try:
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(image_bytes))
        new_width = int(image.width * (width / 100))
        new_height = int(image.height * (height / 100))
        resized_image = image.resize((new_width, new_height))
        with io.BytesIO() as output:
            resized_image.save(output, format="JPEG")
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')
        return processed_image_data
    except Exception as e:
        print(f"\nError during image manipulation: {e}")
        return ""

def rotate_image(encoded_image, angle):
    try:
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(image_bytes))
        rotated_image = image.rotate(angle)
        with io.BytesIO() as output:
            rotated_image.save(output, format="JPEG")
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')
        return processed_image_data
    except Exception as e:
        print(f"\nError during image manipulation: {e}")
        return ""

def apply_blur(encoded_image):
    try:
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(image_bytes))
        blurred_image = image.filter(ImageFilter.GaussianBlur(5))
        with io.BytesIO() as output:
            blurred_image.save(output, format="JPEG")
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')
        return processed_image_data
    except Exception as e:
        print(f"\nError during image manipulation: {e}")
        return ""

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def run_server():
    host = '0.0.0.0'
    port = 8000

    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True)

    server.register_function(convert_to_grayscale, 'convert_to_grayscale')
    server.register_function(resize_image, 'resize_image')
    server.register_function(rotate_image, 'rotate_image')
    server.register_function(apply_blur, 'apply_blur')

    print(f"\nRPC Server has been initialized & awaiting connections {host}:{port}...")
    server.serve_forever()

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nRPC server has been shut down.")
