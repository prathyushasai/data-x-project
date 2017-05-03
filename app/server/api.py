from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from clarifai.client import ClarifaiApi
import os
import json

app = ClarifaiApp("fQejYok0nzGJpuUxGjXKQ62U3ElPSND3F2CRdqSa", "DA9oY3z-s3X8eUUsQQzkmw1aaMBWj-s11QZb-u2C")
clarifai_api = ClarifaiApi("fQejYok0nzGJpuUxGjXKQ62U3ElPSND3F2CRdqSa", "DA9oY3z-s3X8eUUsQQzkmw1aaMBWj-s11QZb-u2C")

# get the general model
model = app.models.get("general-v1.3")

def classify_images(folder):
    images = []
    image_prefix = folder + "/{0}"
    for frame in os.listdir(folder):
        if ".jpg" in frame:
            img = ClImage(file_obj=open(image_prefix.format(frame), 'rb'))
            images.append(img)
    response = model.predict(images)
    return extract_result(response)

def extract_result(response):
    data = response["outputs"][0]["data"]["concepts"]
    result = list()
    # a list of tuples in the form (name, probability)
    for datum in data:
        result.append((datum["name"], datum["value"]))
    return result

def classify(img):
    if ".jpg" in img:
        img = ClImage(file_obj=open(img, 'rb'))
        response = model.predict([img])
        print("classifying {0}".format(img))
        return extract_result(response)
    else:
        raise RuntimeError('not an image: {0}'.format(img))
