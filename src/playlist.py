import os
from googleapiclient.discovery import build
from datetime import timedelta

class PlayList:
    """Класс для видео по id видео"""
    # доступ к переменной окружения с API youtube
    api_key: str = os.getenv('API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)


    def __init__(self, playlist_id: str) -> None:
        """Инициализация экземпляра"""
        self.__playlist_id = playlist_id
        playlist_videos = self.youtube.playlists().list(id=self.__playlist_id,
                                                        part='snippet').execute()
        # название плейлиста
        self.title = playlist_videos['items'][0]['snippet']['title']
        # ссылка на плейлист
        self.url = f'https://www.youtube.com/playlist?list=' \
                   f'{self.__playlist_id}'


    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta`
        с суммарной длительность плейлиста
        """
        # данные по видеороликам в плейлисте
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                            part='contentDetails').execute()
        # все id видеороликов из плейлиста
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        # длительность видеороликов из плейлиста
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id = ','.join(video_ids)).execute()
        durations = [video['contentDetails']['duration'] for video in video_response['items']]
        # сумма длительности видеороликов
        total_duration = sum([timedelta(seconds=int(duration[5:7]),
                                        minutes=int(duration[2:4])) for duration in durations], timedelta())
        return total_duration


    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное
        видео из плейлиста (по количеству лайков)
        """
        # данные по видеороликам в плейлисте
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                            part='contentDetails').execute()
        # все id видеороликов из плейлиста
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        # счетчик лайков
        count = 0
        for video_id in video_ids:
            # статистика видео по id
            video_response = self.youtube.videos().list(part='statistics',
                                                        id=video_id).execute()
            # количество лайков
            like_count = int(video_response['items'][0]['statistics']['likeCount'])
            if like_count > count:
                count = like_count
        return f'https://youtu.be/{video_id}'
