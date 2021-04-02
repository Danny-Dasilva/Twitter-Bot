import re
import random
import cv2
import pytesseract
from PIL import Image, ImageDraw
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


def swipe(width, height):

    x1 = width * random.uniform(.4, .5) 
    y1 = height * random.uniform(.6, .75)
    x2 = width * random.uniform(.4, .5)
    y2 = height * random.uniform(.3, .4)
    device.shell(f'input touchscreen swipe {x1} {y1} {x2} {y2}')

    sleep(1)
# image = device.screencap()
def back(image):
    width, height = image.size 
    x = width * .08
    y = height * .07
    # r = 40 
    # draw = ImageDraw.Draw(image)

    # draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0,255))
    # image.save('back.png', 'PNG')
    sleep(.2)
    click(x, y)
def parse_k(string):
    if 'K' in string:
        val = float(string.split('K')[0])
        val *= 1000

        return int(val)
    if ',' in string:
        return int(string.replace(',', ''))
    else:
        return int(string)
def return_like_cord(img):
    thresh = cv2.inRange(img, (116,116,116, 255), (155,155,155, 255))
    # print(thresh)
    contours, hiearchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = []
    for val in contours:
        area = cv2.contourArea(val)
        if area == 2359.0:
            cnt.append(val)

    cv2.drawContours(img, cnt,-1, (0,255,0), 3)
    cv2.imwrite('example_like_contour.png', img)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area == 2359:
            # print(area, contour)
            cont = np.mean(contour, axis=0)
            # print(area, cont)
            click = cont[0][1]
            yield click
def return_profile_cord(img):
    thresh = cv2.inRange(img, (10,10,10, 255), (255,255,255, 255))
    contours, hiearchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cnt = []
    # for val in contours:
        # area = cv2.contourArea(val)
        # if area > 20000.0:
            # cnt.append(val)
            # print(area)

    # cv2.drawContours(img, cnt,-1, (0,0,255), 3)
    # cv2.imwrite('example_profile_cord.png', img)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 27000.0:
            cont = np.mean(contour, axis=0)
            click = cont[0][1]
            return click
            # yield click

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

    data = np.array(cropped_img) 

    out = return_like_cord(data)  
    for val in out:
        click(center, val)
    return "like" 
def get_account(image):
    width, height = image.size 
    right = width * .2
    center = width * .1
    cropped_img = image.crop((0, 0, right, height)) 

    data = np.array(cropped_img) 

    click_height = return_profile_cord(data)  
    if click_height:
        click(center, click_height)

    
        return get_image()

    else:
        return None



def follow(image):
    width, height = image.size 
    top = height * .2
    bottom = height * .27
    left = width * .7 
    right = width 
    x = (left + right)  / 2
    y = (top + bottom)  / 2
    cropped_img = image.crop((left, top, right, bottom)) 
    data = np.array(cropped_img)
    yer = np.count_nonzero(np.all(data==[0,0,0,255 ],axis=2))
    ratio = yer/ np.count_nonzero(data)
    # ratio of black pixels should be .7 for follow and .18 for unfollow
    if ratio > 0.6:
        click(x, y)
    else:
        pass

def select_latest(image):
    width, height = image.size 
    y = height * .15
    x = width * .28

    click(x, y)
def select_type(image):
    width, height = image.size 
    x = width * .3 

    y = height * .07
    click(x, y)
    
def type(string):
    # select_type(image)
    device.shell("input keyevent 67")     
    device.shell(f'input text {string}')

    device.shell("input keyevent 66")     
def get_follow_ratio(image):
    width, height = image.size 
    top = height * .4
    bottom = height * .75
    left = width * 0  
    right = width * .95
    # left = width * 0.085
    # right = width * .2
    import sys
    # np.set_printoptions(threshold=sys.maxsize)
    cropped_img = image.crop((left, top, right, bottom)) 
    data = np.array(cropped_img)   # "data" is a height x width x 4 numpy array
    cropped_img.save('killme.png', 'PNG')
    thresh = cv2.inRange(data, (10, 100, 200, 255), (155,255,255, 255))
    contours, hiearchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = []
    for val in contours:
        area = cv2.contourArea(val)
        if area == 3267:
            cnt.append(val)
            cont = np.mean(val, axis=0)
            offset = cont[0][1]

    
    cropped_2 = image.crop((left, top + offset - 450, width,top + offset - 200)) 
    cropped_2.save("example_tweet.png", "PNG")
    # cv2.drawContours(data, cnt,-1, (0,255,0), 3)

    # cv2.imwrite('example_tweet.png', data)

    data = np.array(cropped_2)   # "data" is a height x width x 4 numpy array
    # print(data)
    # print(np.where(np.all(data==[217,217,217,255], axis=2)))
    yellowY, yellowX = np.where(np.all(data==[217,217,217,255 ],axis=2))
    # print(yellowY, yellowX)
    
    yellowX = sorted(yellowX)
    yellowY = sorted(yellowY)
    top, bottom = yellowY[0], yellowY[-1]
    left, right = yellowX[0], yellowX[-1]
    # print(top, bottom, "ahh", yellowY[0])
    im2 = Image.fromarray(data)
    # new = im2.crop((0, top -20, width, bottom + 20))
    # new.save('killm2.png', 'PNG')
    read = pytesseract.image_to_string(im2)
    # #remove end of string
    parsed = read.split("Followers")[0]
    following, followers = parsed.split("Following")
    followers = parse_k(followers)
    following = parse_k(following)
    print(f'followers: {followers}, following: {following}')
    return following, followers

def calculate_ratio(following, followers):
    print(following, followers)
    ratio = following/followers
    if ratio > 1.5:
        return True, True
    elif ratio > .85:
        if following > 500:
            return False, True
    else:
        if followers < 100:
            return True, False
        else:
            return False, False
            
# cropped_img.save('like.png', 'PNG')

#write images
# with open('like.png', 'wb') as f:
    # f.write(cropped_img)
# image = Image.open('screen.png')

# Setting the points for cropped image 

def get_image():
    sleep(.4)
    image = device.screencap()

    image = Image.open(io.BytesIO(image))

    return image
def run():
    image = get_image()
    width, height = image.size 
    for i in range(100):
        swipe(width, height)

        image = get_image()
        image = get_account(image)
        if image:
            following, followers = get_follow_ratio(image) 
            like, follow = calculate_ratio(following, followers)
            back(image)

    
    # image = get_account(image)
    # following, followers = get_follow_ratio(image) 
    # calculate_ratio(following, followers)

    # follow(image)
    # select_type(image)
    # type("hello")
    # select_latest(image)
    # swipe(width, height)
    # back(image)
    # get_account(image)

if __name__ == "__main__":
    count = 0 
    run()
    # while count != 100:

        # count += run()
        # sleep(3)
        # print(count)

# device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')
