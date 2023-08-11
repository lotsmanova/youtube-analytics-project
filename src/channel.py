import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб канала"""
    # доступ к переменной окружения с API youtube
    api_key: str = os.getenv('API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey = api_key)


    def __init__(self, channel_id: str) -> None:
        """Инициализация экземпляра"""
        self.__channel_id = channel_id

        self.channel = self.youtube.channels().list(
            id=self.__channel_id, part='snippet,statistics').execute()

        # название канала
        self.title = self.channel['items'][0]['snippet']['title']
        # описание
        self.description = self.channel['items'][0]['snippet']['description']
        # количество просмотров
        self.view_count = self.channel['items'][0]['statistics']['viewCount']
        # количество подписчиков
        self.subscriber_count = int(self.channel['items'][0]['statistics']['subscriberCount'])
        # количество видео
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        # ссылка на канал
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'


    def __str__(self) -> str:
        """Магический метод для строкового представления объекта"""
        return f'{self.title} ({self.url})'


    def __add__(self, other) -> int:
        """Сложение количества подписчиков"""
        return self.subscriber_count + other.subscriber_count


    def __sub__(self, other) -> int:
        """Вычитание количества подписчиков"""
        return self.subscriber_count - other.subscriber_count


    def __gt__(self, other) -> bool:
        """
        Если количество подписчиков 1 канала больше
        количества 2 канала return True.
        Если меньше, False
        """
        return self.subscriber_count > other.subscriber_count


    def __ge__(self, other) -> bool:
        """
        Если количество подписчиков 1 канала больше или равно
        количества 2 канала return True.
        Если меньше, False
        """
        return self.subscriber_count >= other.subscriber_count


    @property
    def channel_id(self) -> str:
        """Геттер для атрибута channel"""
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        # channel = self.youtube.channels().list(
        #     id = self.__channel_id, part = 'snippet,statistics').execute()
        # print(channel)
        print(self.channel)

    @classmethod
    def get_service(cls) -> object:
        """Класс-метод, возвращающий
        объект для с YouTube API"""
        api_key = 'your_api_key'
        youtube = build('youtube', 'v3', developerKey = api_key)
        return youtube


    def to_json(self, filename) -> None:
        """Сохраняет в файл значения атрибутов"""
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
