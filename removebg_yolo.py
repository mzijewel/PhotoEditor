from ultralytics import YOLO
from PIL import Image

def remove(img):
    model=YOLO('yolov8s-seg.pt')
    results=model(img)
    mask=results[0].masks.data[0]
    mask=(mask.numpy()*255).astype('uint8')
    mask=Image.fromarray(mask).resize(img.size)
    new_img=Image.new("RGBA",img.size,0)
    new_img.paste(img,mask=mask)
    return new_img
