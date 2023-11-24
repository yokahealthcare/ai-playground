import cv2
import numpy as np
import torch
from torch2trt import TRTModule

import time


def preprocess_frame(img, img_size=224):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (img_size, img_size))
    img = img.astype('float32')
    img = img / 255.0
    return img


class FightDetector:
    def __init__(self, num_frames=20, num_get=10, img_size=224, threshold=0.5):
        self.num_frames = num_frames
        self.num_get = num_get
        self.img_size = img_size
        self.frames = []
        self.fight = False
        self.model_trt = TRTModule()
        self.model_trt.load_state_dict(torch.load("assets/model/fight/fight_trt.pth"))
        self.model_trt.eval()
        self.threshold = threshold

    def update(self, img):
        img = preprocess_frame(img, self.img_size)
        self.frames.append(img)
        if len(self.frames) > self.num_frames:
            idxs = np.linspace(0, len(self.frames) - 1, self.num_get, dtype=int)
            frames = np.array(self.frames)[idxs]
            frames = np.expand_dims(frames, axis=0)
            frames = torch.from_numpy(frames)
            frames = frames.permute(0, 4, 1, 2, 3)
            t1 = time.time()
            with torch.no_grad():
                frames = frames.cuda()
                logits = self.model_trt(frames)
                logits = torch.sigmoid(logits)
                print(logits, logits.item())
                self.fight = logits.item() >= self.threshold
            t2 = time.time()
            print(f'Fight Inference time: {t2 - t1}')
            self.frames = []

    def plot_frame(self, img):
        if self.fight:
            cv2.putText(img, 'FIGHT', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 2)

        return img


if __name__ == "__main__":
    pass
