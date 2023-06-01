import os
from googleapiclient.discovery import build
class Video:
    """Класс для видео по id видео"""
    # доступ к переменной окружения с API youtube
    api_key: str = os.getenv('API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)


    def __init__(self, id_video: str) -> None:
        """Инициализация экземпляра"""

        # id видео
        self.__id_video = id_video
        video_response = self.youtube.videos().list(
            part='snippet,statistics,contentDetails,topicDetails', id=self.__id_video).execute()

        try:
            # название видео
            self.title = video_response['items'][0]['snippet']['title']
            # ссылка на видео
            self.url = f'https://www.youtube.com/channel/{self.__id_video}'
            # количество просмотров
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            # количество лайков
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            print('Неверный id видео')

            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None


    def __str__(self) -> str:
        """Магический метод для строкового представления объекта"""
        return f'{self.title}'


class PLVideo(Video):
    """Дочерний класс Video"""
    def __init__(self, id_video, id_pl):
        """Инициализация экземпляра"""
        super().__init__(id_video)
        self.id_pl = id_pl