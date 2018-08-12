from . import const
import requests
# import cv2

MSFT_URL = "https://eastus2.api.cognitive.microsoft.com/vision/v1.0/describe"
MSFT_KEY = "e47b133ce1fe416f8af97ba8a9311c37"


def process_image(image):
    pass


def ms_api(image):
    labels = []
    r = requests.post(MSFT_URL,
                      headers={'Content-Type': 'application/octet-stream',
                               'Ocp-Apim-Subscription-Key': MSFT_KEY},
                      data=image).json()
    print(r['description']['tags'])
    if const.FIRE.lower() in r['description']['tags'] or const.FIRE.lower():
        labels.append(const.FIRE)
    elif const.FLOOD.lower() in (r['description']['tags'] or r['description']['text']):
        labels.append(const.FLOOD)
    else:
        return None
    return image, labels


# def draw_bounding_box(img, label, color, x, y, x_plus_w, y_plus_h):
#     cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
#     cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#     return img
