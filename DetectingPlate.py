from src.char_classification.model import CNN_Model
from utils_LP import character_recog_CNN, crop_n_rotate_LP
import cv2
import torch
import numpy as np
from models.experimental import attempt_load
from detect import detect
def crop_LP(source_img, x1, y1, x2, y2, offset=2):
    x1 += offset
    y1 += offset
    x2 -= offset
    y2 -= offset

    cropped_LP = source_img[y1:y2, x1:x2]

    return cropped_LP


def return_crop_img(image_path):
    LP_weights = 'LP_detect_yolov7_500img.pt'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    try:
        model_LP = attempt_load(LP_weights, map_location=device)
    except Exception as e:
        return f"Error loading license plate detection weights: {e}"

    source_img = cv2.imread(image_path)
    if source_img is None:
        return "Image not found or unable to load."

    try:
        pred, LP_detected_img = detect(model_LP, source_img, device, imgsz=640)
    except Exception as e:
        return f"Error during detection: {e}"

    if len(pred) == 0:
        return "No license plate detected."
    else:
        for *xyxy, conf, cls in reversed(pred):
            x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
            try:
                cropped_LP = crop_LP(source_img, x1, y1, x2, y2)
                if cropped_LP is not None:
                    return cropped_LP
            except Exception as e:
                print(f"Error during cropping: {e}")
                continue

    return "No valid license plate found."

def process_license_plate(image_path):
    Min_char = 0.01
    Max_char = 0.09
    CHAR_CLASSIFICATION_WEIGHTS = 'src/weights/weight.h5'
    LP_weights = 'LP_detect_yolov7_500img.pt'

    model_char = CNN_Model(trainable=False).model
    model_char.load_weights(CHAR_CLASSIFICATION_WEIGHTS)

    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    model_LP = attempt_load(LP_weights, map_location=device)

    source_img = cv2.imread(image_path)
    pred, LP_detected_img = detect(model_LP, source_img, device, imgsz=640)

    c = 0
    plate_detected = False
    for *xyxy, conf, cls in reversed(pred):
        x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
        angle, rotate_thresh, LP_rotated = crop_n_rotate_LP(source_img, x1, y1, x2, y2)
        if (rotate_thresh is None) or (LP_rotated is None):
            continue

        #################### Prepocessing and Character segmentation ####################
        LP_rotated_copy = LP_rotated.copy()
        cont, hier = cv2.findContours(rotate_thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        cont = sorted(cont, key=cv2.contourArea, reverse=True)[:17]

        ##################### Filter out characters #################
        char_x = []
        height, width, _ = LP_rotated_copy.shape
        roiarea = height * width

        for ind, cnt in enumerate(cont):
            (x, y, w, h) = cv2.boundingRect(cont[ind])
            ratiochar = w / h
            char_area = w * h

            if (Min_char * roiarea < char_area < Max_char * roiarea) and (0.25 < ratiochar < 0.7):
                char_x.append([x, y, w, h])

        if not char_x:
            continue

        char_x = np.array(char_x)

        ############ Character recognition ##########################

        threshold_12line = char_x[:, 1].min() + (char_x[:, 3].mean() / 2)
        char_x = sorted(char_x, key=lambda x: x[0], reverse=False)
        strFinalString = ""
        first_line = ""
        second_line = ""

        for i, char in enumerate(char_x):
            x, y, w, h = char
            imgROI = rotate_thresh[y:y + h, x:x + w]

            text = character_recog_CNN(model_char, imgROI)
            if text == 'Background':
                text = ''

            if y < threshold_12line:
                first_line += text
            else:
                second_line += text

        strFinalString = first_line + second_line
        plate_detected = True
        break  # Stop processing after the first detected plate

    if plate_detected:
        return strFinalString
    else:
        return "No license plate detected"

# Example usage:
# image_path = 'test_43.jpg'
# result = process_license_plate(image_path)
# print("License Plate Result:", result)