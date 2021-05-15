#!/usr/bin/env python3
import cv2
import numpy as np


def extract(img,n):   #显示某颜色区域
	
	hsv=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
	
	if n==1:
		low=np.array([120,43,46])
		up=np.array([130,255,255])
	if n==2:
		low = np.array([40, 43, 46])
		up = np.array([50, 255, 255])
	if n==3:
		low = np.array([0,43, 46])
		up = np.array([10, 255, 255])
		
	mask=cv2.inRange(hsv,low,up)
	cv2.imshow("1",mask)
	ret, thresh1 = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
	guass=cv2.GaussianBlur(thresh1,(5,5),0)
	cv2.imshow("2",guass)
	kernel = np.ones([5, 5], np.uint8)
	opening = cv2.morphologyEx(guass, cv2.MORPH_OPEN, kernel)
	ret, thresh1 = cv2.threshold(opening, 200, 255, cv2.THRESH_BINARY)
	dst = cv2.erode(thresh1, kernel, iterations=2)
	guass = cv2.GaussianBlur(dst, (9,9), 0)
	ret, thresh1 = cv2.threshold(guass, 200, 255, cv2.THRESH_BINARY)
	dst = cv2.dilate(thresh1,(5,5), iterations=1)
	cv2.imshow("3",thresh1)
	ret, thresh1 = cv2.threshold(guass, 200, 255, cv2.THRESH_BINARY)
	cv2.imshow("4", thresh1)
	contours, hierarchy = cv2.findContours(thresh1, 1, 2)
	print('len(contours):',len(contours))
	temp = [0,0]
	for i in range(0,len(contours)):
		cnt = contours[i]
		print('cnt:',cnt)
		area = cv2.contourArea(cnt)
		print('area:',area)
		if area > temp[0]:
			temp[0] = area
			temp[1] = i
		print('kkkkk')
	img3 = cv2.drawContours(img, contours, temp[1], (255, 0, 0), 3)
	cv2.imshow("end",img3)
	cnt = contours[temp[1]]
	x , y , w ,h = cv2.boundingRect(cnt)
	center_x = x + w/2
	center_y = y + h/2
	print('center_x,center_y:',center_x,center_y)
	im = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	cv2.imshow("co",im)
	if center_x > 220 and center_x < 420:
		return 'ok'
	else:
		return 'no'
	
	
	
	
	
	
color = []
cap=cv2.VideoCapture(1)
#cap.isOpened()
while(1):
	try:
		for i in range(1,4):
			ret, frame = cap.read()
			camera = cv2.imread('5.jpg')
			# cv2.imshow("1", camera)
			cv2.imshow("9", frame)
			#str = extract(camera, 3)
			str = extract(frame, 3)
			print(str)
			if str == 'ok':
				color.append(i)
				print('color:',color)
				break
	except:
		pass
	if cv2.waitKey(30) == ord('q'):
		break
	
	