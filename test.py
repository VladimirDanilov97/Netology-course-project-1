from tokens import  GD_TOKEN, YD_TOKEN, VK_TOKEN, VK_ID
import requests
from pprint import pprint
from photo import Yandex, Vk, upload_vk_photos, GoogleDrive
import json
# upload_vk_photos('552934290', VK_TOKEN, YD_TOKEN, album_id='wall', number_of_photo=3)
g = GoogleDrive(GD_TOKEN)
r = g.upload()
print(r)
# import requests
# headers = {"Authorization": f"Bearer {GD_TOKEN}"}
# para = {
#     "name": "sample.jpg",
# }
# files = {
#     'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
#     'file': open("./sample.jpg", "rb")
# }
# r = requests.post(
#     "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
#     headers=headers,
#     files=files
# )
# print(r.text)