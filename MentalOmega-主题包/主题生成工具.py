#本脚本源于Imaginary MO，by：浅水Shallowaq
#修改/优化：Bt

import PIL
import os
import shutil
import sys
import time
from PIL import Image, ImageGrab, ImageDraw, ImageFont, ImageFilter

#高斯模糊，就是所谓的毛玻璃


#说明
print("本脚本源于Imaginary MO，by：浅水Shallowaq\n修改/优化：Bt\n----------------------")
#设置保存的主题序号
#保存路径

print("默认安装情况下：\n[Gura]古拉主题[默认] - 1\n[ATRI]亚托莉主题 - 2\n[RAIN]雨天主题 - 3\n[Neko]甘城猫猫 - 4\n[Mobius]梅比乌斯 - 5\n[Sakura]樱花猫娘-6\n[City]市区少女 - 7\n[AngDem]天使与恶魔 - 8\n[helSpr]温泉猫娘 - 9\n[Ganyu]甘雨/离月 - 10\n----------------------\n请尽可能使用16：10比例图片\n")
print("输入的那个数字意思是指替换掉那个主题，仅支持10个主题并存\n")
Theme = input("输入要保存的主题数字[1至10]，并按回车键：")
#创建文件夹
def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
    # 复制
def copy_file(file_old_path, file_new_path):
    for root, dirs, files in os.walk(f'{file_old_path}'):
        for file in files:
            src_file = os.path.join(root, file)
            shutil.copy(src_file, f'{file_new_path}')

def del_file(path_data):
    for i in os.listdir(path_data) :
        file_data = path_data + "\\" + i
        if os.path.isfile(file_data) == True:
            os.remove(file_data)
        else:
            del_file(file_data)

os.system("cls")
#print("默认安装情况下：\n[Gura]古拉主题[默认] - 1\n[ATRI]亚托莉主题 - 2\n[RAIN]雨天主题 - 3\n[Neko]甘城猫猫 - 4\n[Mobius]梅比乌斯 - 5\n[Sakura]樱花猫娘-6\n[City]市区少女 - 7\n[AngDem]天使与恶魔 - 8\n[helSpr]温泉猫娘 - 9\n[Ganyu]甘雨/离月 - 10      \n1 - 直接保存到主题(覆盖现有装载主题)\n2 - 保存到游戏目录下的out文件夹里")
print("\n直接保存到主题(覆盖现有装载主题) - 1\n另存到游戏目录下的out文件夹里 - 2\n----------------------")
Save_as = input("输入数字按回车：")
#让生成的图片直接覆盖到主题
if int(Save_as) == 1:
    Save_path = f"./Resources/Manager/TP/{Theme}"
    Save_path_MM = f"./Resources/Manager/MainMenu/{Theme}"
    Save_pathB = "./Resources/Manager/TP/"
    mkdir(f"./Resources/Manager/TP/{Theme}")

#让生成的图片打包成主题并放到out里
if int(Save_as) == 2:
    Save_path = f"./out/Resources/Manager/TP/{Theme}"
    Save_path_MM = f"./out/Resources/Manager/MainMenu/{Theme}"
    Save_pathB = "./out/Resources/Manager/TP/"
    mkdir(f"./out/Resources/Manager/TP/{Theme}")
    mkdir(f"./out/Resources/Manager/MainMenu")

# Save_path = "./out/Resources/Manager/TP/{Theme}"
# Save_path_MM = "./Resources/Manager/MainMenu/{Theme}"
os.system("cls")
class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=20, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)

print('主题生成中……请等待下一步操作……')

#生成结果输出文件夹
mkdir("./Resources/result/")
#输出路径
extra_path=".//Resources//result//"
ui_bg = Image.open("MainMenu.png").convert("RGBA")
#背景图片尺寸重置
ui_bg = ui_bg.resize((1280, 768), resample=Image.LANCZOS)

#左半部分高斯模糊
ui_left = ui_bg.crop(box=(0,0,200,768))
ui_left_mask = Image.new('RGBA',(200,768),(96,96,96,64))
ui_left.paste(ui_left_mask,(0,0),mask=ui_left_mask)
ui_left=ui_left.filter(MyGaussianBlur(radius=20))

# #绘制MO水印
# ui_mo_mark = Image.new('RGBA',(300,40),(255,255,255,0))
# draw = ImageDraw.Draw(ui_mo_mark)
# font = ImageFont.truetype('Aspergit.ttf', 40)
# draw.text((0,0), 'Mental Omega', font=font, fill=(255,255,255,128))
# ui_mo_mark = ui_mo_mark.rotate(90,expand=1)
# ui_left.paste(ui_mo_mark,(160,458),mask=ui_mo_mark)

#绘制渐变边缘
for i in range(0,10):
    alpha = 255-int(255/10*i)
#    sidelight = Image.new('RGBA',(1,200),(210,235,238,alpha))
    #uplight = Image.new('RGBA',(200,1),(210,235,238,alpha))
    borderlight = Image.new('RGBA',(1,768),(160,160,160,alpha))
#    ui_left.paste(sidelight,(i,0),mask=sidelight)
#    ui_left.paste(uplight,(0,i),mask=uplight)
#    ui_left.paste(uplight,(0,768-i),mask=uplight)
    ui_left.paste(borderlight,(200-i,0),mask=borderlight)
    


#去透明度
for i in range(0,200):
    for j in range(0,768):
        r,g,b,a = ui_left.getpixel((i,j))
        ui_left.putpixel((i,j),(r,g,b,255))

#组合保存
ui_bg.paste(ui_left,(0,0))
for i in range(0,10):
    alpha = 255-int(255/10*i)
    sidelight = Image.new('RGBA',(1,768),(210,235,238,alpha))
    ui_bg.paste(sidelight,(1280-i,0),mask=sidelight)
#ui_bg.save("mainmenubg.png")

#在线标题绘制
ui_ol = Image.new('RGBA',(140,70),(255,255,255,0))
title = Image.open(".\Resources\Manager\online.png").convert("RGBA")
#size = 140

# # 绘制四角
# for i in range(0, 10):
#     alpha = int(255 / 8 * min((10 - i), 8))
#     sidelight = Image.new('RGBA', (1, 20), (26, 244, 254, alpha))
#     uplight = Image.new('RGBA', (20, 1), (26, 244, 254, alpha))
#     ui_ol.paste(uplight, (0, 10 + i), mask=uplight)
#     ui_ol.paste(uplight, (0, 70 - i - 1), mask=uplight)
#     ui_ol.paste(uplight, (size - 20, 10 + i), mask=uplight)
#     ui_ol.paste(uplight, (size - 20, 70 - i - 1), mask=uplight)
#
#     ui_ol.paste(sidelight, (i, 10), mask=sidelight)
#     ui_ol.paste(sidelight, (size - i - 1, 10), mask=sidelight)
#     ui_ol.paste(sidelight, (i, 50), mask=sidelight)
#     ui_ol.paste(sidelight, (size - i - 1, 50), mask=sidelight)

#组合标题
ui_ol.paste(title,(30,0),mask=title)
ui_bg.paste(ui_ol,(-28,20),mask=ui_ol)
ui_bg.save(extra_path+"mainmenubg.png")
#ui_ol.save("ol2.png")


# #逐一打开按钮
# campaign = Image.open(".//MainMenu//campaign.png").convert("RGBA")
# cncnet = Image.open(".//MainMenu//cncnet.png").convert("RGBA")
# exitgame = Image.open(".//MainMenu//exitgame.png").convert("RGBA")
# lan = Image.open(".//MainMenu//lan.png").convert("RGBA")
# loadmission = Image.open(".//MainMenu//loadmission.png").convert("RGBA")
# mapeditor = Image.open(".//MainMenu//mapeditor.png").convert("RGBA")
# options = Image.open(".//MainMenu//options.png").convert("RGBA")
# skirmish = Image.open(".//MainMenu//skirmish.png").convert("RGBA")
# statistics = Image.open(".//MainMenu//statistics.png").convert("RGBA")
#
# fb = Image.open("menu_fb1.png").convert("RGBA")
# yt = Image.open("menu_yt1.png").convert("RGBA")
# tw = Image.open("menu_tw1.png").convert("RGBA")
# dc = Image.open("menu_dc1.png").convert("RGBA")
#
# ex = Image.open(".//MainMenu//extras.png").convert("RGBA")
#
# #按钮拼接
# ui_bg.paste(campaign,(10,210),mask=campaign)
# ui_bg.paste(skirmish,(10,262),mask=skirmish)
# ui_bg.paste(cncnet,(10,314),mask=cncnet)
# ui_bg.paste(lan,(10,366),mask=lan)
# ui_bg.paste(loadmission,(10,418),mask=loadmission)
# ui_bg.paste(options,(10,470),mask=options)
# ui_bg.paste(mapeditor,(10,522),mask=mapeditor)
# ui_bg.paste(statistics,(10,574),mask=statistics)
# ui_bg.paste(exitgame,(10,626),mask=exitgame)
#
# ui_bg.paste(fb,(15,728),mask=fb)
# ui_bg.paste(yt,(45,728),mask=yt)
# ui_bg.paste(tw,(75,728),mask=tw)
# ui_bg.paste(dc,(105,728),mask=dc)
#
# ui_bg.paste(ex,(1250,354),mask=ex)
#
# #保存拼接后的UI
# ui_bg.save(extra_path+"fullmainmenubg.png")

# window_w = [1200,600,600,300,576,600,800,700]
# window_h = [720,450,380,240,435,600,600,520]
# #生成cncnetlobbybg hotkeyconfigbg loadmissionbg
# window_name = ['cncnetlobbybg','hotkeyconfigbg','loadmissionbg','logindialogbg','optionsbg','privatemessagebg','missionselectorbg','scoreviewerbg']
# window_shade = [160,96,160,96,96,96,160,96]


#仅生成三个即可
window_w = [1117,583,800]
window_h = [639,439,600]
window_name = ['cncnetlobbybg','hotkeyconfigb','loadmissionbg']
window_shade = [160,170,50]

#窗口毛玻璃化
for i in range(0,3):
    stx,sty,enx,eny = 640-int(window_w[i]/2),384-int(window_h[i]/2),640+int(window_w[i]/2),384+int(window_h[i]/2)
    #print(str(stx)+" "+str(sty)+" "+str(enx)+" "+str(eny))
    ui_window = ui_bg.crop(box=(stx,sty,enx,eny))
    ui_window_mask = Image.new('RGBA',(int(window_w[i]),int(window_h[i])),(window_shade[i],window_shade[i],window_shade[i],64))
    ui_window.paste(ui_window_mask,(0,0),mask=ui_window_mask)
    ui_window=ui_window.filter(MyGaussianBlur(radius=30))
    
    #绘制渐变边缘
    for j in range(0,10):
        alpha = 255-int(255/10*j)
        sidelight = Image.new('RGBA',(1,window_h[i]),(210,235,238,alpha))
        uplight = Image.new('RGBA',(window_w[i],1),(210,235,238,alpha))
        ui_window.paste(sidelight,(j,0),mask=sidelight)
        ui_window.paste(uplight,(0,j),mask=uplight)
        ui_window.paste(uplight,(0,window_h[i]-j),mask=uplight)
        ui_window.paste(sidelight,(window_w[i]-j,0),mask=sidelight)
    
    #去透明度    
    for j in range(0,window_w[i]-1):
        for k in range(0,window_h[i]-1):
            r,g,b,a = ui_window.getpixel((j,k))
            ui_window.putpixel((j,k),(r,g,b,255))   
        
    ui_window.save(extra_path+window_name[i]+'.png')
#将重复要处理的图片复制为两份，减少处理时间
shutil.copyfile(f'.\\Resources\\result\\cncnetlobbybg.png',f".\\Resources\\result\\gamelobbybg.png")
shutil.copyfile(f'.\\Resources\\result\\hotkeyconfigb.png',f".\\Resources\\result\\optionsbg.png")
shutil.copyfile(f'.\\Resources\\result\\loadmissionbg.png',f".\\Resources\\result\\missionselectorbg.png")
os.system("cls")
#处理完后转储
if int(Save_as) == 1:
    del_file(f".\Resources\Manager\TP\{Theme}")
    os.remove(f'.\\Resources\\Manager\\MainMenu\\{Theme}.pbt')
    shutil.copyfile('.\\Resources\\result\\mainmenubg.png', f".\Resources\Manager\MainMenu\{Theme}.pbt")
    os.remove('.\\Resources\\result\\mainmenubg.png')
    copy_file(r".\Resources\result\mainmenubg.png", f".\Resources\Manager\MainMenu\{Theme}")
    copy_file(r".\Resources\result",f".\Resources\Manager\TP\{Theme}")
    print("\n成功生成，请在'主题包控制器'里查看或更换\n")
else:
    del_file(f".\out\Resources\Manager\TP\{Theme}")
    os.remove(f'.\\out\\Resources\\Manager\\MainMenu\\{Theme}.pbt')
    shutil.copyfile('.\\Resources\\result\\mainmenubg.png', f".\out\Resources\Manager\MainMenu\{Theme}.pbt")
    os.remove('.\\Resources\\result\\mainmenubg.png')
    copy_file(r".\Resources\result\mainmenubg.png", f".\out\Resources\Manager\MainMenu\{Theme}")
    copy_file(r".\Resources\result", f".\out\Resources\Manager\TP\{Theme}")
    print("\n成功生成，请在游戏目录的out文件夹里查看或更换\n")
del_file(r".\Resources\result")


#生成主题包名字
Theme_name = input("给你的主题起个名字吧：")
with open(f"{Save_pathB}{Theme}.name",'w')as file:
        file.write(f'{Theme_name}')

#打开
#image3 = Image.open("head3.png")

#重置大小
#imager = image.resize((1000, 200), resample=Image.LANCZOS)

#组合图片
#imager.paste(image2, (0, 0), mask=image2)

#保存图片
#imager.save("top3.png")

#绘制文字
#draw = ImageDraw.Draw(image4)
#font = ImageFont.truetype('kyokasho.ttf', 30)
#draw.text((190,90), '一只天上的大萝卜', font=font, fill=(192,64,128))

#绘制文字大小
#draw = ImageDraw.Draw(image4)
#font = ImageFont.truetype('kyokasho.ttf', 30)
#sizex = draw.textsize('一只天上的大萝卜')

#制图
#image5 = Image.new('RGB', (1000, 800), (255, 255, 255))

#裁切
#imagen = image5.crop(box=(0,0,18,20))

#画线
#draw = ImageDraw.Draw(image5)
#shape = [(50,250), (400,250)]