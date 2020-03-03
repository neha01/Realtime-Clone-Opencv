# pylint: skip-file
""" Stitch image in realtime webcam feed """
import numpy as np 
import cv2
from PIL import Image

class RealtimeImageStitching():
    """ Stitch image in realtime webcam feed """
    
    def stitch_images(self, img, flip_img):
        """ accepts two images and returns concatenated image horizontally"""
        img_pil = self.convert_to_pil_img(img)
        flip_img_pil = self.convert_to_pil_img(flip_img)
        images = [img_pil, flip_img_pil]
        x_offset = 0
        total_img_width = sum([image.size[0] for image in images])
        total_img_height = max([image.size[1] for image in images])
        stitched_img_pil = Image.new('RGB', (total_img_width, total_img_height))
        for img in images:
            stitched_img_pil.paste(img, (x_offset, 0))
            x_offset += img.size[0]
        stitched_img_np = np.asarray(stitched_img_pil)
        return stitched_img_np

    def convert_to_pil_img(self, img):
        """ converts image to PIL format """
        return Image.fromarray(img)

    def convert_bgr_to_rgb_img(self,img):
        """ converts image from BGR to RGB format """
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def main():
    """ driver function """
    cap = cv2.VideoCapture(0)
    count = 0
    img_width = 700
    img_height = 700
    image_stitching = RealtimeImageStitching()
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        count += 1
        resized_img = cv2.resize(frame, (img_width, img_height))
        resized_flip_img = cv2.flip( resized_img, 1)
        resized_img = image_stitching.convert_bgr_to_rgb_img(resized_img)
        resized_flip_img = image_stitching.convert_bgr_to_rgb_img(resized_flip_img)
        stitched = image_stitching.stitch_images(resized_img, resized_flip_img )
        stitched = cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB)
        cv2.imshow('stitched Image ', stitched)
        if cv2.waitKey(10) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows

main()


