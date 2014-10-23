import pygame.camera
import pygame.image
import pygame.transform

from requests_toolbelt import MultipartEncoder
import requests

import clipboard
import os
from time import ctime

PUUSH_DOMAIN = os.getenv("PUUSH_DOMAIN", "https://puush.me")

def capture_image():
    pygame.camera.init()
    cam = pygame.camera.Camera(0,(640,480))
    cam.start()
    img = cam.get_buffer()
    fn = "WebcamCapture-{}.jpg".format(ctime().replace(":", "-").replace(" ", "_"))
    pygame.image.save(pygame.transform.flip(pygame.image.frombuffer(img[0], (img[1],img[2]), "RGB"),False,True), fn)
    cam.stop()
    return fn

def upload_image(filename, key=None):
    if not key:
        return "-3"
    m = MultipartEncoder(fields={"k": key,
                                 "z": "poop",
                                 "f": (filename, open(filename, 'rb'), 'application/octet-stream')})
    return requests.post(PUUSH_DOMAIN + "/api/up", data=m, headers={"Content-Type": m.content_type}).text

if __name__ == "__main__":
    fn = capture_image()
    out = upload_image(fn, key=os.getenv("PUUSH_KEY", None)).split(",")
    if len(out) > 1:
        print out[1]
        clipboard.copy(out[1])
    else:
        if out[0] == "-1":
            print "Upload failure"
        elif out[0] == "-2":
            print "No filename header"
        elif out[0] == "-3":
            print "You need to add PUUSH_KEY as an environment variable, with your api key"
    os.unlink(fn)