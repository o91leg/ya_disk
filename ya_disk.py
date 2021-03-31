import requests
import os

TOKEN = 'Ваш токен'

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get('href', '')
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')
        else:
            print('Fail')

if __name__ == '__main__':
    uploader = YaUploader(token=TOKEN)
    user_input = input('Введите путь к файлу с расширением: ')
    user_input_name = input('Введите имя которое будет созданно на яндекс диске с расширением: ')
    path_user, filename = os.path.split(user_input)
    os.chdir(path=path_user)
    uploader.upload_file_to_disk(user_input_name, filename)

