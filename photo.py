import requests
import json
import datetime
from progress.bar import IncrementalBar
from tokens import YD_TOKEN, VK_TOKEN, GD_TOKEN


class Vk():
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version,
        }

    def get_photo_by_id(self, owner_id=None,
                        album_id='profile', extended='1',
                        photo_sizes='0'):
        method = 'photos.get'
        get_photo_url = self.url + method
        get_photo_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': extended,
            'photo_sizes': photo_sizes,
        }
        params = self.params
        params.update(get_photo_params)
        req = requests.get(get_photo_url, params=params).json()
        return req['response']['items']

    def get_maxsized_photo(self, owner_id=None, album_id='profile', ):
        photos = self.get_photo_by_id(owner_id=owner_id, album_id=album_id)
        result = []
        names = set()
        for item in photos:
            max_size = item['sizes'][0]
            for size in item['sizes']:
                if size['height'] >= max_size['height'] and \
                   size['width'] >= max_size['width']:
                    max_size = size
            name = str(item['likes']['count'])
            if name not in names:
                names.add(name)
            else:
                date = datetime.datetime.utcfromtimestamp(int(item['date']))
                name = name + '_' + date.strftime('%Y-%m-%d_%H-%M')
            result.append({
                'file_name': name,
                'size_type': max_size['type'],
                'max_size': max([max_size['height'], max_size['width']]),
                'url': max_size['url']
            })
        return result


class Yandex():
    url = url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.headers = {
            "Authorization": f'{token}'
        }

    def create_folder(self, path):
        url = self.url + 'resources'
        headers = self.headers
        params = {
            'path': path,
        }
        response = requests.put(url, headers=headers, params=params, timeout=3)
        if 200 <= response.status_code < 300:
            return 'Create folder successfuly'

    def upload(self, file_url, filename, path='/course_project_1/'):
        url = self.url + 'resources/upload'
        params = {
            'path': path+filename,
            'url': file_url,
            'overwrite': 'true',
        }
        headers = self.headers
        self.create_folder(path)
        response = requests.post(url, headers=headers,
                                 params=params, timeout=5)
        if 200 <= response.status_code < 300:
            return f'{filename} upload successfully'
        else:
            return response.status_code


class GoogleDrive():
    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType="

    def __init__(self, token):
        self.headers = {
           'Authorization': f'Bearer {token}',
        }

    def upload(self, file_url, file_name, path: list):
        params = {
            'name': file_name,
            'parents': path
        }
        url = self.url + 'multipart'
        files = {
            'data': ('metadata', json.dumps(params),
                     'application/json; charset=UTF-8'),
            'file': requests.get(file_url).content,
        }
        headers = self.headers
        response = requests.post(url, headers=headers, files=files, timeout=5)
        if 200 <= response.status_code < 300:
            return f'{file_name} upload successfully'
        else:
            return response.status_code


def upload_photos_from_vk(id, drive, vk_token, token,
                          album_id='profile',
                          path='/course_project_1/',
                          number_of_photo=5):
    vk_client = Vk(VK_TOKEN, '5.131')
    if drive == 'Google':
        client = GoogleDrive(token)
    elif drive == 'Yandex':
        client = Yandex(token)

    album_photos = vk_client.get_maxsized_photo(str(id), album_id=album_id)
    photos_to_upload = sorted(album_photos,
                              key=lambda i: i['max_size'],
                              reverse=True)[:number_of_photo]
    bar = IncrementalBar('Files uploaded', max=len(photos_to_upload))
    for photo in photos_to_upload:
        client.upload(photo['url'], photo['file_name'], path)
        bar.next()
    bar.finish()
    with open('output.json', 'w') as file:
        json.dump([{
                    'name': x['file_name'],
                    'size': x['size_type']
                    } for x in photos_to_upload], file, indent=4)


if __name__ == '__main__':
    path = ['1QcTNN7UteEtKIHoIvEMz6QLR6Uy8Mg5r']
    upload_photos_from_vk('552934290', 'Google',
                          VK_TOKEN, GD_TOKEN,
                          path=path, number_of_photo=3)
    upload_photos_from_vk('552934290', 'Yandex',
                          VK_TOKEN, YD_TOKEN,
                          number_of_photo=3)
