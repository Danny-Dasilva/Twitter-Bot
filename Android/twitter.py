import re
import cv2
import pytesseract
from PIL import Image
from ppadb.client import Client
import numpy as np

import io
from time import sleep


def skip(width, height):
    x = width * .75
    y = height * .84

    device.shell(f"input tap {x} {y}")

def download(width, height):
    x = width * .95
    y = height * .84
    # print(f"adb shell input tap {x} {y}")
    device.shell(f"input tap {x} {y}")
    # device.shell(f"input tap {x} {y}")
    
    sleep(1)
    x = width * .85
    y = height * .51
    device.shell(f"input tap {x} {y}")
    sleep(2)
    skip(width, height)
def crop_image(image, width, height):
    top = height / 1.8 
    bottom = top + (height/10) 
     
    cropped_img = image.crop((0, top, width, bottom)) 
    # im1.save('screen1.png', 'PNG')
    return cropped_img



adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()
device = devices[0]
# device.shell('input touchscreen swipe 500 500 500 500')

# image = device.screencap()

def parse_k(string):
    if 'K' in string:
        val = int(string.split('K')[0])
        val *= 1000
        return val
    if ',' in string:
        return int(string.replace(',', ''))
    else:
        return int(string)
def return_like_cord(img):
    thresh = cv2.inRange(img, (116,116,116, 255), (155,155,155, 255))
    print(thresh)
    contours, hiearchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 2000:
            # print(area, contour)
            cont = np.mean(contour, axis=0)
            print(area, cont)
            click = cont[0][1]
            yield click
    # cv2.drawContours(img, cn, -1, (0,255,0), 3)
    # cv2.imshow('image', img)
    # cv2.imwrite('image.png', img)
    # cv2.waitKey(0)
def click(x, y):
    device.shell(f"input tap {x} {y}")
def get_like(image):
    width, height = image.size 
    top = height * .47
    bottom = height * .51
    left = width * 0.6
    right = width * .665
    center = width * .63
    cropped_img = image.crop((left, 0, right, height)) 
    print(image.size)

    data = np.array(cropped_img) 

    out = return_like_cord(data)  
    for val in out:
        click(center, val)
    # TO DO
    #get specific color
    #loop up through 
    #check dimensions of upwards cube

    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
    
    # Replace white with red... (leaves alpha values alone...)
    # white_areas = (red < 216) | (blue < 216) | (green < 216)
    # data[..., :-1][white_areas.T] = (0, 0, 0) # Transpose back needed
    # white_areas = (red > 216) & (blue > 216) & (green > 216)
    # data[..., :-1][white_areas.T] = (255, 0, 0) # Transpose back needed
    # Find X,Y coordinates of all yellow pixels

    # yellowY, yellowX = np.where(np.all(data>=[10,10,10, 255],axis=2))

    # top, bottom = min(yellowY), max(yellowY)
    # left, right = min(yellowX), max(yellowX) 
    # print(top, bottom, left, right, )
    # new = cropped_img.crop((left, top, right, bottom)) 
    # # print(np.array(new))
    # image.save('test.png', 'PNG')


    # result = np.any(data != [0, 0, 0, 255], axis=-1)
    # result = data[data != result]
    # print(result)
    return "like" 


def get_follow_ratio(image):
    width, height = image.size 
    top = height * .45
    bottom = height * .6
    left = width * 0  
    right = width * .95
    cropped_img = image.crop((0, top, width, bottom)) 
    print(image.size)

    data = np.array(cropped_img)   # "data" is a height x width x 4 numpy array
    # red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
    
    # Replace white with red... (leaves alpha values alone...)
    # white_areas = (red < 216) | (blue < 216) | (green < 216)
    # data[..., :-1][white_areas.T] = (0, 0, 0) # Transpose back needed
    # white_areas = (red > 216) & (blue > 216) & (green > 216)
    # data[..., :-1][white_areas.T] = (255, 0, 0) # Transpose back needed
    # Find X,Y coordinates of all yellow pixels
    yellowY, yellowX = np.where(np.all(data>=[216,216,216],axis=2))

    top, bottom = yellowY[0], yellowY[-1]
    left, right = yellowX[0], yellowX[-1]

    im2 = Image.fromarray(data)
    new = im2.crop((0, top -20, width, bottom + 20))
    # new.save('test.png', 'PNG')
    read = pytesseract.image_to_string(new)
    # #remove end of string
    print(read)
    parsed = read.split("Followers")[0]
    following, followers = parsed.split("Following")
    followers = parse_k(followers)
    following = parse_k(following)
    print(f'followers:{followers}, following:{following}')
    return following, followers

def calculate_ratio(following, followers):
    print(following, followers)
    ratio = following/followers
    print(ratio)
    if ratio > 1.5:
        print("follow")
        print("like")
    elif ratio > .75:
        if following > 500:
            print("follow")
        else:
            print("like")
    else:
        if followers < 100:
            print("follow")
        else:
            return False
# cropped_img.save('like.png', 'PNG')

#write images
# with open('like.png', 'wb') as f:
    # f.write(cropped_img)
# image = Image.open('screen.png')

# Setting the points for cropped image 

def call():
    print(percentage)
    if percentage < 0.48:

        im = crop_image(image, width, height)
        read = pytesseract.image_to_string(im)
        print(read)
        search = 'North Texas'
        if search in read or 'Clock' in read or 'UNT' in read:
            print('donwload')
            download(width, height)
            return 1
        else:
            print('skip')
            skip(width, height)
            return 0
    else:
        print("already liked")
        skip(width, height)
        return 0 


def run():
    image = device.screencap()

    image = Image.open(io.BytesIO(image))
    width, height = image.size 
    # following, followers = get_follow_ratio(image) 
    # calculate_ratio(following, followers)
    get_like(image)

if __name__ == "__main__":
    count = 0 
    run()
    # while count != 100:

        # count += run()
        # sleep(3)
        # print(count)

# device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')
