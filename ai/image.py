from . import const
import requests
# import cv2

MSFT_URL = "https://eastus.api.cognitive.microsoft.com/vision/v1.0/describe?maxCandidates=1"
MSFT_KEY = "7b86593b414d4a5eb5096115cf2f7d55"


def process_image(image):
    pass


def ms_api(image):
    labels = []
    r = requests.post(MSFT_URL,
                      headers={'Content-Type': 'application/octet-stream',
                               'Ocp-Apim-Subscription-Key': MSFT_KEY},
                      data=image).json()
    if const.FIRE.lower() in r['description']['tags']:
        labels.append(const.FIRE)
    if const.FLOOD.lower() in r['description']['tags']:
        labels.append(const.FLOOD)
    else:
        return None
    return image, labels


# def draw_bounding_box(img, label, color, x, y, x_plus_w, y_plus_h):
#     cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
#     cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#     return img
