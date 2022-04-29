# coding=utf-8
from pprint import pprint
import requests


class YaUploader:
    HOST = 'https://cloud-api.yandex.net:443'

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'}

    def get_files_list(self):
        url = f'{self.HOST}/v1/disk/resources/files/'
        headers = self.get_headers()
        params = {'fields': 'items.name, items.size'}
        response = requests.get(url, headers=headers, params=params).json()
        pprint(response)

    def _get_upload_link(self, path):
        url = f'{self.HOST}/v1/disk/resources/upload/'
        headers = self.get_headers()
        params = {'path': path, 'overwrite': True}
        response = requests.get(url, headers=headers, params=params).json()
        pprint(response)
        return response.get('href')

    def upload_file(self, path, file_name):
        upload_link = self._get_upload_link(path)
        headers = self.get_headers()
        response = requests.put(upload_link, data=open(file_name, 'rb'), headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print('Upload success')


if __name__ == '__main__':
    FILE_NAME = 'file-to-drive.txt'
    TOKEN = ''
    uploader = YaUploader(TOKEN)
    uploader.upload_file(f'/{FILE_NAME}', FILE_NAME)
