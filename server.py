from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from PIL import Image
import io
import base64

def process_image(image_data, option):
    try:
        # Decodificar os dados da imagem
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        print(f"Recebida operação {option} para processar a imagem.")

        if option == '1':
            # Transformar a imagem em preto e branco
            image = image.convert('L')
        elif option == '2':
            # Rodar a imagem em 90 graus
            image = image.rotate(90)
        elif option == '3':
            # Mudar as dimensões da imagem para 200x200 pixels
            image = image.resize((200, 200))

        # Salvar a imagem processada
        with io.BytesIO() as output:
            image.save(output, format="JPEG")
            processed_image_data = base64.b64encode(output.getvalue()).decode('utf-8')

        print(f"Operação {option} concluída. Enviando a imagem processada de volta para o cliente.")

        return processed_image_data
    except Exception as e:
        print(f"Erro durante o processamento da imagem: {e}")
        return ""  # Retorna uma string vazia em caso de erro

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def run_server():
    host = 'localhost'  # Altere para o endereço desejado
    port = 8000  # Altere para a porta desejada

    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler)

    server.register_function(process_image, 'process_image')

    print(f"Server awaiting connections {host}:{port}...")
    server.serve_forever()

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("RPC server has been shut down.")
