import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб канала"""
    #доступ к переменной окружения с API youtube
    api_key: str = os.getenv('API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey = api_key)


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
            Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        channel = self.youtube.channels().list(
            id=self.__channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.view_count = channel['items'][0]['statistics']['viewCount']
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'


    @property
    def channel_id(self):
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(
            id = self.__channel_id,part = 'snippet,statistics').execute()
        print(channel)


    @classmethod
    def get_service(cls):
        api_key = 'your_api_key'
        youtube = build('youtube', 'v3', developerKey = api_key)
        return youtube


    def to_json(self, filename):
        '''сохраняет в файл значения атрибутов'''
        data = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'view_count': self.view_count,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'url': self.url
            }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
