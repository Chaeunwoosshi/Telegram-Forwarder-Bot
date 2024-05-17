import os

from telethon import events


class Forward:
    def __init__(self, client, forward_config_map):
        self.client = client
        self.forward_config_map = forward_config_map
        self.client.add_event_handler(self.message_handler, events.NewMessage(chats=list(forward_config_map.keys())))
        self.client.add_event_handler(self.album_handler, events.Album(chats=list(forward_config_map.keys())))

    async def message_handler(self, event):
        if event.grouped_id:
            return
        destination_id = self.forward_config_map.get(event.chat_id).destinationID
        await self.send_message(destination_id, event.message)

    async def album_handler(self, event):
        destination_id = self.forward_config_map.get(event.chat_id).destinationID
        await self.send_album(destination_id, event)

    async def send_message(self, destination_channel_id, message):
        media_path = None
        if message.media:
            media_path = await self.download_media(message)
        text = message.text if message.text else ''
        if media_path:
            await self.client.send_file(destination_channel_id, media_path, caption=text)
            self.delete_media(media_path)
        else:
            await self.client.send_message(destination_channel_id, text)

    async def send_album(self, destination_channel_id, event):
        media_path_list = []
        for message in event.messages:
            if message.media:
                media_path = await self.download_media(message)
                media_path_list.append(media_path)
        await self.client.send_file(destination_channel_id, media_path_list, caption=event.text)
        for media_path in media_path_list:
            self.delete_media(media_path)

    async def download_media(self, message):
        download_folder = 'media'
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        file_path = await self.client.download_media(message, file=download_folder)
        return file_path

    def delete_media(self, media_path):
        os.remove(media_path)
