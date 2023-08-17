import configparser
import os
from pyrogram import Client
from pyrogram.handlers import MessageHandler

# Configurações iniciais
CONFIG_FILE = 'config.ini'
SESSION_FILE_FMT = 'user'
MAX_FILE_SIZE = 4000 * 1024 * 1024  # 4000MB

def config_exists():
    config = configparser.ConfigParser()
    return config.read(CONFIG_FILE)

def get_api_credentials():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config['Credentials']['api_id'], config['Credentials']['api_hash']

def save_api_credentials(api_id, api_hash):
    config = configparser.ConfigParser()
    config['Credentials'] = {'api_id': api_id, 'api_hash': api_hash}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def save_state(file_name, source_channel, destination_channel, destination_folder, last_message_id):
    with open(file_name, 'w') as f:
        f.write(f"source_channel:{source_channel}\n")
        f.write(f"destination_channel:{destination_channel}\n")
        f.write(f"destination_folder:{destination_folder}\n")
        f.write(f"last_message_id:{last_message_id}\n")

def load_state(file_name):
    data = {}
    with open(file_name, 'r') as f:
        for line in f:
            key, value = line.strip().split(':')
            data[key] = value     
    return data['source_channel'], data['destination_channel'], data['destination_folder'], int(data['last_message_id'])

def download_progress(current, total):
    print(f"Baixando mídia, andamento do download {(current / total) * 100:.1f}%")

async def clone_channel_messages(app, source_channel_id, destination_channel_id, file_name, last_message_id=None):
    messages = []

    async for message in app.get_chat_history(source_channel_id):
        messages.append(message)

    reversed_messages = list(reversed(messages))

    # Encontre o índice da última mensagem clonada
    last_index = None
    for index, message in enumerate(reversed_messages):
        if message.id == last_message_id:
            last_index = index
            break

    # Se encontrou a última mensagem, comece a partir do próximo índice
    if last_index is not None:
        messages_to_clone = reversed_messages[last_index + 1:]
    else:
        messages_to_clone = reversed_messages

    for message in messages_to_clone:
        print(f"Tentando encaminhar mensagem {message.id}...")
        
        try:
            if message.caption:
                caption = message.caption
            else:
                caption = ""

            caption += f"\n\nCanal clonado usando ProtectClone, download do script em @DevWHub"

            if message.photo:
                await app.send_photo(destination_channel_id, message.photo.file_id, caption=caption)
                print("Mídia enviada com sucesso.")
            elif message.video:
                await app.send_video(destination_channel_id, message.video.file_id, caption=caption)
                print("Vídeo enviado com sucesso.")
            elif message.document:
                await app.send_document(destination_channel_id, message.document.file_id, caption=caption)
                print("Vídeo enviado com sucesso.")
            elif message.animation:
                await app.send_animation(destination_channel_id, message.animation.file_id, caption=caption)
                print("Vídeo enviado com sucesso.")
            elif message.sticker:
                await app.send_sticker(destination_channel_id, message.sticker.file_id)
                print("Vídeo enviado com sucesso.")
            elif message.text:
                await app.send_message(destination_channel_id, message.text + "\n\nCanal clonado usando ProtectClone, download do script em @DevWHub")
                print("Mensagem encaminhada com sucesso.")
            last_message_id = message.id
        except Exception as e:
            print(f"Erro ao encaminhar mensagem: {e}")
            if "CHAT_FORWARDS_RESTRICTED" in str(e):
                print("Erro de restrição de encaminhamento, tentando baixar mídia...")
                try:
                    path = ''
                    if message.photo:
                        path = await message.download(progress=download_progress)
                        await app.send_photo(destination_channel_id, path, caption=caption)
                    elif message.video:
                        path = await message.download(progress=download_progress)
                        await app.send_video(destination_channel_id, path, caption=caption)
                    elif message.document:
                        path = await message.download(progress=download_progress)
                        await app.send_document(destination_channel_id, path, caption=caption)                            
                    elif message.audio:
                        path = await message.download(progress=download_progress)
                        await app.send_audio(destination_channel_id, path, caption=caption)                            
                    elif message.voice:
                        path = await message.download(progress=download_progress)
                        await app.send_voice(destination_channel_id, path, caption=caption)                            
                    elif message.animation:
                        path = await message.download(progress=download_progress)
                        await app.send_animation(destination_channel_id, path, caption=caption)                            
                    elif message.sticker:
                        await app.send_sticker(destination_channel_id, message.sticker.file_id)
                    elif message.text:
                        await app.send_message(destination_channel_id, message.text + "\n\nCanal clonado usando ProtectClone, download do script em @DevWHub")
                    os.remove(path)
                    print("Mídia ou mensagem enviada com sucesso.")
                    last_message_id = message.id
                except Exception as e:
                    print(f"Erro ao processar mídia: {e}")
        save_state(file_name, source_channel_id, destination_channel_id, None, last_message_id)

async def clone_message(app, message, destination_channel_id, mention):
    try:
        if message.caption:
            caption = message.caption
        else:
            caption = ""

        caption += f"\n\nPostagem clonada usando ProtectClone, download do script em @DevWHub"

        if mention == 1:
            await message.forward(destination_channel_id)
        elif mention == 2:
            if message.photo:
                await app.send_photo(destination_channel_id, message.photo.file_id, caption=caption)
            elif message.video:
                await app.send_video(destination_channel_id, message.video.file_id, caption=caption)
            elif message.document:
                await app.send_document(destination_channel_id, message.document.file_id, caption=caption)                            
            elif message.audio:
                await app.send_audio(destination_channel_id, message.audio.file_id, caption=caption)                            
            elif message.voice:
                await app.send_voice(destination_channel_id, message.voice.file_id, caption=caption)                            
            elif message.animation:
                await app.send_animation(destination_channel_id, message.animation.file_id, caption=caption)                            
            elif message.sticker:
                await app.send_sticker(destination_channel_id, message.sticker.file_id)
            elif message.text:
                await app.send_message(destination_channel_id, message.text + "\n\nCanal clonado usando ProtectClone, download do script em @DevWHub")
        print("Mensagem clonada com sucesso.")
    except Exception as e:
        print(f"Erro ao encaminhar mensagem: {e}")
        if "CHAT_FORWARDS_RESTRICTED" in str(e):
            print("Erro de restrição de encaminhamento, tentando baixar mídia...")
            try:
                path = ''
                if message.photo:
                    path = await message.download(progress=download_progress)
                    await app.send_photo(destination_channel_id, path, caption=caption)
                elif message.video:
                    path = await message.download(progress=download_progress)
                    await app.send_video(destination_channel_id, path, caption=caption)
                elif message.document:
                    path = await message.download(progress=download_progress)
                    await app.send_document(destination_channel_id, path, caption=caption)                            
                elif message.audio:
                    path = await message.download(progress=download_progress)
                    await app.send_audio(destination_channel_id, path, caption=caption)                            
                elif message.voice:
                    path = await message.download(progress=download_progress)
                    await app.send_voice(destination_channel_id, path, caption=caption)                            
                elif message.animation:
                    path = await message.download(progress=download_progress)
                    await app.send_animation(destination_channel_id, path, caption=caption)                            
                elif message.sticker:
                    await app.send_sticker(destination_channel_id, message.sticker.file_id)
                elif message.text:
                    await app.send_message(destination_channel_id, message.text + "\n\nCanal clonado usando ProtectClone, download do script em @DevWHub")
                os.remove(path)
                print("Mídia ou mensagem enviada com sucesso.")
            except Exception as e:
                print(f"Erro ao processar mídia: {e}")

listen_source_id = None
listen_destination_id = None
mention = 1

async def chat_listener(client, message):
    if message.chat.id == listen_source_id:
        try:
            print("Nova mensagem detectada. Clonando...")
            await clone_message(client, message, listen_destination_id, mention)
            print("Mensagem clonada com sucesso.")
        except Exception as e:
            print(f"Erro ao clonar mensagem: {e}")

async def download_chat_files(app, source_channel, file_name, destination_folder, last_message_id=0):
    messages = []

    async for message in app.get_chat_history(source_channel):
        messages.append(message)

    reversed_messages = list(reversed(messages))

    # Encontre o índice da última mensagem clonada
    last_index = None
    for index, message in enumerate(reversed_messages):
        if message.id == last_message_id:
            last_index = index
            break

    # Se encontrou a última mensagem, comece a partir do próximo índice
    if last_index is not None:
        messages_to_clone = reversed_messages[last_index + 1:]
    else:
        messages_to_clone = reversed_messages

    for message in messages_to_clone:
        print(f"Tentando baixar arquivo {message.id}...")
        file_counter = message.id
        print(f"Baixando arquivo {file_counter}...")
        
        try:
            # Obter a extensão do arquivo da mídia
            if message.photo:
                media_extension = 'jpg'
            if message.video:
                # Obtém o MIME type do vídeo
                mime_type = message.video.mime_type

                # Determina a extensão do vídeo com base no MIME type
                if mime_type.startswith("video/"):
                    media_extension = mime_type.replace("video/", "")
                    print(f"Extensão do vídeo: {media_extension}")
            if message.document:
                # Obtém o MIME type do documento
                mime_type = message.document.mime_type

                # Obtém a extensão do arquivo a partir do MIME type
                media_extension = mime_type.split('/')[-1]

                print(f"Extensão do documento: {media_extension}") 
            # Define o nome do arquivo com base no contador e na extensão da mídia
            destination_path = os.path.join(destination_folder, f"arquivo {str(file_counter).zfill(3)}.{media_extension}")
            await message.download(file_name=destination_path, progress=download_progress)
            print(f"Arquivo {file_counter} baixado com sucesso.")
            last_message_id = message.id
            save_state(file_name, source_channel, None, destination_folder, last_message_id)             
        except Exception as e:
            print(f"Erro ao baixar o arquivo: {e}")


def main():
    if not config_exists():
        api_id = input("Informe o API ID: ")
        api_hash = input("Informe o API Hash: ")
        save_api_credentials(api_id, api_hash)
    else:
        api_id, api_hash = get_api_credentials()

    session_file = SESSION_FILE_FMT

    print("Conectado com sucesso!")
    print("Selecione o modo:")
    print("1. Modo Clonador")
    print("2. Modo Chat Listener")
    print("3. Modo Chat Downloader")
    mode_choice = input("Escolha o modo (1, 2 ou 3): ")
    if mode_choice == '1':
        with Client(session_file, api_id=api_id, api_hash=api_hash) as app:
            # Modo Clonador
            choice = input("Deseja iniciar do zero ou continuar a clonagem? (digite '0' para começar do zero ou '1' para continuar): ")
            if choice == '0':
                file_name = input("Informe um nome para o arquivo da clonagem atual: ") + '.txt'
                source_channel = input("Informe o username ou ID do canal origem (ex: @YourSourceChannel): ")
                destination_channel = input("Informe o username ou ID do canal de destino (ex: @YourDestinationChannel): ")
                # Verifica se o source_channel e destination_channel são números e os converte em int, caso contrário, mantém como estão
                if source_channel.startswith("-") and source_channel[1:].isdigit():
                        source_channel = int(source_channel)
                if destination_channel.startswith("-") and destination_channel[1:].isdigit():
                    destination_channel = int(destination_channel)

                save_state(file_name, source_channel, destination_channel, None, 0)  # 0 representa que não há última mensagem
                app.run(clone_channel_messages(app, source_channel, destination_channel, file_name, last_message_id=0))
            else:
                file_name = input("Informe o nome do arquivo a partir do qual deseja continuar a clonagem: ") + '.txt'
                if os.path.exists(file_name):
                    source_channel, destination_channel, destination_folder, last_message_id = load_state(file_name)
                    
                    # Verifica se o source_channel e destination_channel são números e os converte em int, caso contrário, mantém como estão
                    if source_channel.startswith("-") and source_channel[1:].isdigit():
                        source_channel = int(source_channel)
                    if destination_channel.startswith("-") and destination_channel[1:].isdigit():
                        destination_channel = int(destination_channel)
                    
                    app.run(clone_channel_messages(app, source_channel, destination_channel, file_name, last_message_id=last_message_id))
                else:
                    print("Arquivo não encontrado.")
                    return
    elif mode_choice == '2':
        app = Client(session_file, api_id=api_id, api_hash=api_hash)
        global listen_source_id
        global listen_destination_id
        global mention
        source_channel = input("Informe o username ou ID do canal origem (ex: @YourSourceChannel): ")
        destination_channel = input("Informe o username ou ID do canal de destino (ex: @YourDestinationChannel): ")

        # Verifica se o source_channel e destination_channel são números e os converte em int, caso contrário, mantém como estão
        if source_channel.startswith("-") and source_channel[1:].isdigit():
            source_channel = int(source_channel)
        if destination_channel.startswith("-") and destination_channel[1:].isdigit():
            destination_channel = int(destination_channel)
            
        print("Você deseja mencionar o autor da mensagem ou deseja ocular?")
        print(f"Digite 1 para mencionar\nDigite 2 para ocultar")
        mention = int(input("Selecione uma opção:"))
        listen_source_id = int(source_channel)
        listen_destination_id = int(destination_channel)
        app.add_handler(MessageHandler(chat_listener))
        app.run()
    elif mode_choice == '3':
        with Client(session_file, api_id=api_id, api_hash=api_hash) as app:
            # Modo Clonador
            choice = input("Deseja iniciar do zero ou continuar o download? (digite '0' para começar do zero ou '1' para continuar): ")
            if choice == '0':
                destination_folder = input("Informe um nome para a pasta de download: ")
                file_name = destination_folder + '.txt'
                source_channel = input("Informe o username ou ID do canal origem (ex: @YourSourceChannel): ")
                # Verifica se o source_channel e destination_channel são números e os converte em int, caso contrário, mantém como estão
                if source_channel.startswith("-") and source_channel[1:].isdigit():
                    source_channel = int(source_channel)

                save_state(file_name, source_channel, None, destination_folder, 0)  # 0 representa que não há última mensagem
                app.run(download_chat_files(app, source_channel, file_name, destination_folder, last_message_id=0))
            else:
                destination_folder = input("Informe o nome da pasta onde o download estava sendo feito: ")
                file_name = destination_folder + '.txt'
                if os.path.exists(file_name):
                    source_channel, destination_channel, destination_folder, last_message_id = load_state(file_name)
                    
                    # Verifica se o source_channel e destination_channel são números e os converte em int, caso contrário, mantém como estão
                    if source_channel.startswith("-") and source_channel[1:].isdigit():
                        source_channel = int(source_channel)
                    
                    app.run(download_chat_files(app, source_channel, file_name, destination_folder, last_message_id=last_message_id))
                else:
                    print("Arquivo não encontrado.")
                    return


if __name__ == "__main__":
    main()