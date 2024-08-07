import numpy as np
from janim.items.image_item import VideoFrame
from PIL import Image, ImageChops


def get_diff_pic(t1, t2) -> Image.Image:
    f1 = VideoFrame('2024/VideoEncoding/assets/example.mp4', t1)
    f2 = VideoFrame('2024/VideoEncoding/assets/example.mp4', t2)

    img1 = f1.image.get()
    img2 = f2.image.get()
    diff = ImageChops.difference(img1, img2)
    return diff


# get_diff_pic(0, 0.1).save('2024/VideoEncoding/assets/diff.jpg')
