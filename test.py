from tokens import YD_TOKEN, VK_TOKEN, VK_ID
import requests
from pprint import pprint
from photo import Yandex, Vk, upload_vk_photos


upload_vk_photos('552934290', VK_TOKEN, YD_TOKEN)