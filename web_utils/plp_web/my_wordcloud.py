
import random 
import math
from turtle import position
 
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def random_col1(): 
    return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)
 
def find_position(img,size_x,size_y):
    integral = np.cumsum(np.cumsum(np.asarray(img),axis=1),axis=0)
    for x in range(1,648-size_x):
        for y in range(1,480-size_y):
            area = integral[y-1,x-1] + integral[y+size_y-1,x+size_x -1]
            area -= integral[y-1,x+size_x-1] + integral[y+size_y-1,x-1]
            if not area:
                return x,y
    return None,None

def save_wordcloud(words, product, platform):
    img = Image.new('L',(648,480))
    draw = ImageDraw.Draw(img)
    res_img = Image.new('L',(648,480),color='white')
    res_img = res_img.convert('RGBA')
    res_draw = ImageDraw.Draw(res_img)
    for word in words:
        font_size = random.randint(50,150)
        font = ImageFont.truetype('C:\Windows\Fonts\SIMHEI.TTF', font_size)
        box_size = draw.textsize(word,font=font)
        x,y = find_position(img,box_size[0],box_size[1])
        if x:
            draw.text((x,y),word,fill='white',font=font)
            res_draw.text((x,y,0,0),word,fill=(random_col1()),font=font)

    res_img = res_img.convert("RGB")
    res_img.save('../app/static/images/'+product+'_'+platform+'_wordcloud.jpg')