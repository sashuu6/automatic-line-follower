import cv2
import numpy as np

MIN_MATCH_COUNT = 30
# feature extractor
detector = cv2.xfeatures2d.SIFT_create()
FLANN_INDEX_KDTREE = 0
flannParam = dict(algorithm=FLANN_INDEX_KDTREE, tree=5)
# feature matcher, takes in flannParam and empty dictionary(opencv bug)
flann = cv2.FlannBasedMatcher(flannParam, {})

trainImg = cv2.imread("TrainingImage.jpg", 0)  # 0 makes it grayscale
# detector will return key point and descriptor
# (trainKP)key point are cordinates where you find the feature
# (trainDecs) descriptor is a description of the key points (size, orientation, direction)
trainKP, trainDecs = detector.detectAndCompute(trainImg, None)

cam = cv2.VideoCapture(0)  # captures webcam image
while True:
    ret, QueryImgBGR = cam.read()  # captures frame from camera
    # convert to grayscale
    QueryImg = cv2.cvtColor(QueryImgBGR, cv2.COLOR_BGR2GRAY)
    queryKP, queryDesc = detector.detectAndCompute(QueryImg, None)
    matches = flann.knnMatch(queryDesc, trainDecs, k=2)  # 2 by default
    # knmMatch will give random matches, find parts which are not in image
    # m is the queryMatch
    # n is the train match

    goodMatch = []
    for m, n in matches:
        if(m.distance < 0.75*n.distance):
            goodMatch.append(m)  # finds good matches and adds it to a list

    if(len(goodMatch) > MIN_MATCH_COUNT):
        # draws a box around the image
        tp = []
        qp = []
        for m in goodMatch:
            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)
        tp, qp = np.float32((tp, qp))
        H, status = cv2.findHomography(tp, qp, cv2.RANSAC, 3.0)
        h, w = trainImg.shape
        trainingBorder = np.float32([[[0, 0], [0, h-1], [w-1, h-1], [0, w-1]]])

        queryBorder = cv2.perspectiveTransform(trainingBorder, H)
        cv2.polylines(QueryImgBGR, [np.int32(
            queryBorder)], True, (0, 255, 0), 5)
    else:
        # %(len(goodMatch),MIN_MATCH_COUNT)
        print("Not enough matches - %d/%d")
    cv2.imshow('result', QueryImgBGR)
    cv2.waitKey(10)
