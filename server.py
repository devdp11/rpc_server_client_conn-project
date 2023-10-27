import xmlrpc.server
from PIL import Image
import io
import base64
from PIL import ImageFilter

def convert_image(encoded_image):
    try:
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(image_bytes))
        original_format = image.format
        image = image.convert('L')
        with io.BytesIO() as output:
            image.save(output, format=original_format)
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')
        return processed_image_data
    except Exception as e:
        print(f"\nError during image operation: {e}")
        return ""

def rotate_image(encoded_image, angle):
    try:
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(image_bytes))
        original_format = image.format
        rotated_image = image.rotate(angle)
        with io.BytesIO() as output:
            rotated_image.save(output, format=original_format)
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')
        return processed_image_data
    except Exception as e:
        print(f"\nError during image operation: {e}")
        return ""
        
def resize_image(encoded_image, width, height):
    try:
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(image_bytes))
        original_format = image.format
        image = image.resize((width, height), Image.LANCZOS)
        with io.BytesIO() as output:
            image.save(output, format=original_format)
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')
        return processed_image_data
    except Exception as e:
        print(f"\nError during image operation: {e}")
        return ""

def blur_image(encoded_image):
    try:
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(io.BytesIO(image_bytes))
        original_format = image.format
        image = image.filter(ImageFilter.GaussianBlur(5))
        with io.BytesIO() as output:
            image.save(output, format=original_format)
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')
        return processed_image_data
    except Exception as e:
        print(f"\nError during image operation: {e}")
        return ""

server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True)
server.register_function(convert_image, 'convert_image')
server.register_function(resize_image, 'resize_image')
server.register_function(rotate_image, 'rotate_image')
server.register_function(blur_image, 'blur_image')

print(f"\nRPC Server has been initialized on port 8000...")
server.serve_forever()
