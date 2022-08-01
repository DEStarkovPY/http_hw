from pprint import pprint
import requests
import os


# # №1
# sh_api_url = 'https://akabab.github.io/superhero-api/api'
# sh_responce = requests.get(sh_api_url)
# pprint(sh_responce.json())

# №2
class YaUploader:
    def __init__(self, token: str):
        self.token = token
        
    def get_headers(self):
        return{
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self):
        """Метод загружает файлы по списку file_list из яндекс диска"""
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        my_headers = self.get_headers()
        responce = requests.get(files_url, headers=my_headers)
        return pprint(responce.json())
    
    def get_upload_link(self, disk_file_path: str): # - функция, получающая ссылку, по которой нужно загрузить файл
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        my_headers = self.get_headers()
        my_params = {'path': disk_file_path, 'overwrite': 'true'} # - первый параметр отвечает за то, куда положить файл, а второй о том, что при значении True файл, если он там есть, будет перезаписан
        responce = requests.get(upload_url, headers=my_headers, params=my_params)
        return responce.json()
        
    
    def upload(self, disk_file_path, file_name):
        href = self.get_upload_link(disk_file_path=disk_file_path).get('href', '')
        responce = requests.put(href, data=open(file_name, 'rb')) # - загрузка файла на яндекс диск в байтевом виде
        responce.raise_for_status() # - если приходит неправильный код ответа, то будет сформированна ошибка
        if responce.status_code == 201:
            print('Success')
def file_path(file_name: str):
    """Функция, получающая путь до файла при вводе его имени и расширения"""
    THIS_PATH = os.getcwd()
    full_path = os.path.join(THIS_PATH, file_name)
    return full_path


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = file_path('upload_file.txt')
    token = ''
    uploader = YaUploader(token)
    result = uploader.upload('netology/upload_file.txt', path_to_file)


# №3
site_url = 'https://api.stackexchange.com/docs/questions'
site_params = {'fromdate' : '1659139200', 'todate' : '1659312000', 'order' : 'desc', 'sort' : 'activity', 'tagged' : 'Python', 'site' : 'stackoverflow'}
responce = requests.get(site_url, params=site_params)
# pprint(responce.json())