import xmlrpc.client
import os
import base64

def send_image_and_option(image_path, option):
    try:
        # ...

        # Chamar a função do servidor RPC
        processed_image_data = server.process_image(image_data, option)

        if processed_image_data is not None:
            with open('processed_image.jpg', 'wb') as processed_image_file:
                processed_image_file.write(base64.b64decode(processed_image_data))

            print("Imagem processada recebida e salva como 'processed_image.jpg'.")
        else:
            print("Erro durante o processamento da imagem no servidor.")
    except Exception as e:
        print(f"Erro: {e}")



if __name__ == "__main__":
    image_path = input("Insira o caminho da imagem: ")

    if not os.path.isfile(image_path):
        print("Arquivo de imagem não encontrado.")
    else:
        print("Escolha uma opção:")
        print("1 - Transformar a imagem em preto e branco")
        print("2 - Rodar a imagem")
        print("3 - Mudar as dimensões da imagem")

        option = input("Opção: ")

        if option in ('1', '2', '3'):
            send_image_and_option(image_path, option)
        else:
            print("Opção inválida.")
