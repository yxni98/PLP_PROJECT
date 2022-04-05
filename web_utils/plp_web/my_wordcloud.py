
import random 
import math
 
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
 
def find_position(img,size_x,size_y):
    #返回给定轴上的累积和numpy.cumsum（a，axis = None，dtype = None，out = None ）
    #0为纵轴，1为横轴
    #assarray()创建ndarray数组对象
    integral = np.cumsum(np.cumsum(np.asarray(img),axis=1),axis=0)
    for x in range(1,800-size_x):
        for y in range(1,600-size_y):
            #左上角小矩形+大矩形(矩阵行对应y，列对应x)
            area = integral[y-1,x-1] + integral[y+size_y-1,x+size_x -1]
            #减去左侧矩形和上方矩形
            area -= integral[y-1,x+size_x-1] + integral[y+size_y-1,x-1]
            #area为0,返回（x,y)
            if not area:
                return x,y
    #返回为空
    return None,None

#循环将词语绘制到图像上
def main():
    #词语素材
    words = ['作者','高度','浓缩','中国','西北','农村','历史',\
        '变迁','过程','作品','思想','艺术','高度','统一','主人公','面对','困境','艰苦','奋斗','精神', '合成', '卷轴', '没事', '人家', '邮寄']
    #新建画布对象，Image.new(mode,size,color=None)
    img = Image.new('L',(800,600))
    #新建画布绘画对象
    draw = ImageDraw.Draw(img)
    for word in words:
        #字体大小随机
        font_size = random.randint(50,150)
        #字体为黑体
        font = ImageFont.truetype('C:\Windows\Fonts\SIMHEI.TTF', font_size)
 
        #计算文字矩形框的大小(宽x,高y)
        box_size = draw.textsize(word,font=font)
 
        #图像上找出文字放置的位置
        x,y = find_position(img,box_size[0],box_size[1])
 
        #存在x，则将词语放置在（x，y）处
        if x:
            draw.text((x,y),word,fill="white",font=font)
    img.show()
 
if __name__ == '__main__':
    main()