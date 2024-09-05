#!/full/path/to/.venv/bin/python3
import re
import sys
import os, time

from telethon import TelegramClient, events

api_id = 
api_hash = ""
client = TelegramClient("mmpc", api_id, api_hash)
message = " ".join(sys.argv[1:])
download_dir = "/path/to/music"


async def download_media(event):

    media = event.message.media
    name = event.media.document.attributes[1].file_name
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(download_dir + "/" + name):
        await client.download_media(media, download_dir)

    print(f"Media file downloaded to {download_dir}")
    os.system("mpc update")
    os.system("mpc ls telegram")
    os.system("mpc add example_directory")
    await client.disconnect()


with client as client:
    client.loop.run_until_complete(client.send_message("https://t.me/fmusbot", message))

    @client.on(
        events.NewMessage(pattern=sys.argv[1], from_users="https://t.me/fmusbot")
    )
    async def handle_message(event):
        sender = await event.get_sender()
        messages = await client.get_messages(sender.username)
        await messages[0].click(0)

    @client.on(
        events.NewMessage(
            pattern=rf"^(?!{message}).*", from_users="https://t.me/fmusbot"
        )
    )
    async def handle_message(event):
        if event.message.media:
            await download_media(event)
        else:
            time.sleep(1)
            await client.send_message("https://t.me/fmusbot", message)


client.start()
client.run_until_disconnected()
