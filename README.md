# License-Plate-Recognition-YOLOv7-and-CNN

<p align="center"><img src="doc/input_img.jpg" width="500"></p>
<p align="center"><i>Figure. Input license plate </i></p>

<p align="center"><img src="doc/LP_detected_img.png" width="500"></p>
<p align="center"><i>Figure. Final result </i></p>

## Table of contents
* [1. Introduction](#2-Introduction)
* [2. License Plate Detection](#3-License-Plate-Detection)
* [3. Hough Transform Alignment](#4-Hough-Transform-Alignment)
* [4. Character Segmentation and Recognition](#5-Character-Segmentation-and-Recognition)
* [5. Conclusion](#6-Conclusion)


## 1. Introduction
As you know: **There are 3 main stages in the license plate recoginition algorithm**

1. License Plate Detection
2. Character Segmentation
3. Character Recognition

<p align="center"><img src="https://user-images.githubusercontent.com/40959407/130982072-a4701080-e40d-42c1-8fc5-062da340ca5b.png" width="300"></p>
<p align="center"><i>Figure. The main stages in the license plate recoginition algorithm </i></p>

## 2. License Plate Detection
Difference form my previous repo. I detected LP with just image preprocessing. It was quite complicated and low accuracy. But now with YOLOv7, all we have to do is collecting the data and train the model

1. Instead of taking a lot of pictures for training, I recoreded the video and use `vid2img.py` to split frames into images
2. I used [labelImg](https://github.com/heartexlabs/labelImg#create-pre-defined-classes) to label each images. We will have the `.txt` file in the same folder with the image. `.txt` file include label, x, y, w, h
3. Split the dataset into 70/20/10
4. Train YOLOv7 on Kaggle 

You can find the whole dataset and the code on my kaggle: [YOLO V7 License Plate Detection](https://www.kaggle.com/code/bomaich/yolo-v7-license-plate-detection)

**[Dataset](https://www.kaggle.com/datasets/bomaich/vnlicenseplate) include 1000 images of both 1 and 2 lines Vietnamese License Plates**

The result is quite good

<p align="center"><img src="doc/License_plate_cropped.png" width="200"></p>
<p align="center"><i>Figure. Detected License Plate </i></p>

## 3. Hough Transform Alignment

With previous repo, I tried to find the biggest contour, and from 4 coordinates of that contour, I can rotate the License Plate; however, it has 2 problems with contour
* Not sure that the biggest contour is the LP. Somtimes the view is not good which is hard to find the right contour
* Not sure that we can approx that contour to 4 points. If not, we can't calculate the rotate angle

Now I come up with different approach. 
1. I used Hough transform to find the horizontal lines 
2. Using some criterias (length, angle...) to find the right ones
3. Calculate angles and `angles.mean()`
4. Rotate the LP with `angles.mean()`

<p align="center"><img src="doc/HoughLP.png" width="300">            <img src="doc/rotate_img.png" width="300"></p>
<p align="center"><i>Figure. Rotated License Plate </i></p>

## 4. Character Segmentation and Recognition

Here I used the same technique as before. I won't talk much about this part, because so many people have done that
1. Find contours
2. Filter out the right contour
3. Recognize with CNN

<p align="center"><img src="doc/LP crop and rotate.png" width="300">            <img src="doc/imgROI.png" width="100"></p>
<p align="center"><i>Figure. Find and extract characters </i></p>

<p align="center"><img src="doc/char segment 2.png" width="400"></p>
<p align="center"><i>Figure. Character segmentation result </i></p>

## 5. Conclusion

<p align="center"><img src="doc/final_result 2.png" width="500">            <img src="doc/LP_detected_img.png" width="500"></p>
<p align="center"><i>Figure. Final results </i></p>
