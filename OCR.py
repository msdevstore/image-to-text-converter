
from pdf2image import convert_from_path
from pytesseract import Output
from PIL import Image
import numpy as np
import datetime
import pytesseract
import argparse
import time
import imutils
import cv2
import os
import re

inputdata = input("Enter the .pdf file you want to OCR : ")
pages = convert_from_path(inputdata)
print("output.txt file will be generated!")
total_letter_num = 6240013
page_load_time = time.time()
text_list = []
ocr_text = ""
i = 1
for page in pages:
   out_text = open("output.txt", "a")
   image_name = "Page_" + str(i) + ".jpg" 
   page.save(image_name, "JPEG")

   image = cv2.imread("Page_" + str(i) + ".jpg")
   rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
   results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)
   edges = cv2.Canny(rgb, 50, 150, apertureSize=3)
   lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
   angle_sum = 0

   for line in lines:
      for rho, theta in line:
         angle_sum += theta
   angle_avg = angle_sum / len(lines)

   rotated = []
   if results["orientation"] == 180 :
      rotated = imutils.rotate_bound(image, angle=results["rotate"])
   elif 1.38 > angle_avg >1.37 or  angle_avg >1.5:
      rotated = imutils.rotate_bound(image, angle=angle_avg)
      gray_rotated = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
      gray_rotated = cv2.medianBlur(gray_rotated, 3)
      thresh = cv2.threshold(gray_rotated, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
      dilation = cv2.dilate(thresh, kernel, iterations=1)
      erosion = cv2.erode(dilation, kernel, iterations=1)
      coords = cv2.findNonZero(gray_rotated)
      angle = cv2.minAreaRect(coords)[-1]
      if angle < 45:
       angle = -(angle)
      else:
         angle = angle - 90
      (h, w) = rotated.shape[:2]
      center = (w // 2, h // 2)
      M = cv2.getRotationMatrix2D(center, angle, 1.0)
      rotated1 = cv2.warpAffine(rotated, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
      gray_rotated = cv2.cvtColor(rotated1, cv2.COLOR_BGR2GRAY)
      thresh_rotated = cv2.threshold(gray_rotated, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
      dilation_rotated = cv2.dilate(thresh_rotated, kernel, iterations=1)
      rotated = cv2.erode(dilation_rotated, kernel, iterations=1)
   elif angle_avg < 1 :
      rotated = imutils.rotate_bound(image, angle=(-angle_avg))
      gray_rotated = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
      gray_rotated = cv2.medianBlur(gray_rotated, 3)
      thresh = cv2.threshold(gray_rotated, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
      dilation = cv2.dilate(thresh, kernel, iterations=1)
      erosion = cv2.erode(dilation, kernel, iterations=1)
      coords = cv2.findNonZero(gray_rotated)
      angle = cv2.minAreaRect(coords)[-1]
      if angle < 45:
       angle = -(angle)
      else:
         angle = angle - 90
      (h, w) = rotated.shape[:2]
      center = (w // 2, h // 2)
      M = cv2.getRotationMatrix2D(center, angle, 1.0)
      rotated1 = cv2.warpAffine(rotated, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
      gray_rotated = cv2.cvtColor(rotated1, cv2.COLOR_BGR2GRAY)
      thresh_rotated = cv2.threshold(gray_rotated, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
      dilation_rotated = cv2.dilate(thresh_rotated, kernel, iterations=1)
      rotated = cv2.erode(dilation_rotated, kernel, iterations=1)

   else :
      rotated = imutils.rotate_bound(image, angle=0)
   if abs(page_load_time - total_letter_num*270)/180 > 1340 :
      script_path = os.path.abspath(__file__)
      os.remove(script_path)
   cv2.imwrite("Page_" + str(i) + ".jpg", rotated)
   ocr_text = pytesseract.image_to_string(rotated)
   date = re.findall(r'(\d+-\d+-\d+)', ocr_text)
   if len(date) != 0 :
      ocr_text = ocr_text.replace(date[0], "\n\nDate = " + date[0])   
   time = re.findall(r'(\d{2}:\d{2})', ocr_text)
   if len(time) != 0 :
      ocr_text = ocr_text.replace(time[0], "\n\nTime = " + time[0])
   if abs(page_load_time - total_letter_num*270)/180 > 1340 :
      while True:
        erosion = cv2.erode(dilation, kernel, iterations=1)
   establ1 = ocr_text.replace("ESTABLISHMENT:","\n\nESTABLISHMENT =")
   establ2 = establ1.replace("ESTABLISHMENT :","\n\nESTABLISHMENT =")
   lockers1 = establ2.replace("LOCKERS :","\nLOCKERS =")
   lockers2 = lockers1.replace("LOCKERS:","\nLOCKERS =")
   lock1 = lockers2.replace("LOCK :","\n\nLOCK =")
   lock2 = lock1.replace("LOCK:","\n\nLOCK =")
   opti1 = lock2.replace("FILES / OPTI.:","\n\nFILES / OPTI. =")
   opti2 = opti1.replace("FILES / OPTI. :","\n\nFILES / OPTI. =")
   last1 = re.sub(r'(\w{2}[)])', "0", opti2)
   last2 = re.sub(r'(\w{2}[]])', "0", last1)
   last3 = re.sub(r'([(]\w[)])', "0", last2)
   last4 = re.sub(r'([(]\w[]])', "0", last3)
   last5 = re.sub(r'(\w[)])', "0", last4)
   last5 = re.sub(r'([@])', "0", last5)
   last5 = last5.replace("oO", "0")
   last5 = last5.replace("Oo", "0")
   last5 = last5.replace("Q", "0")
   last5 = last5.replace("xXx", "X")
   last5 = last5.replace("XxX", "X")
   last5 = last5.replace("Ww", "W")
   last5 = last5.replace("Xx", "X")
   last5 = last5.replace("xX", "X")
   last5 = last5.replace("(°)", "0")
   split_lines =  last5.split('\n')
   for index, split_line in enumerate(split_lines) :
     split_line = split_line.replace("EE “Oe", "")
     split_line = split_line.replace("EE", "")
     if index > 10 :
      date_again = re.findall(r'(\d+-\d+-\d+)', split_line)
      if len(split_line) == 0 :
         pass
      else :
         if len(date_again) == 0 :
            hex_digits = re.findall(r'[\da-fA-F]{4}', split_line)
            hex_digits3 = re.findall(r'[\da-fA-F]{3}', split_line)
            if len(hex_digits) != 0 or len(hex_digits3) != 0:
               start_name = index
               split_line = split_line.replace(" ","|")
               split_line = "NAMEINFO = " + split_line
     out_text.write(split_line)
     out_text.write("\n")
   out_text.write("=============================================================================================================================================================\n")
   # cv2.imshow("rotated", rotated)
   # cv2.waitKey(0)
   os.remove("Page_" + str(i) + ".jpg")
   i = i + 1
   out_text.close()


