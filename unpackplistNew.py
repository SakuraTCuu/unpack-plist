# -*- coding: utf-8 -*-
import os,sys
from xml.etree import ElementTree
from PIL import Image
#C:\Users\HP\Desktop\unpackerPlist\unpack-plist\number.plist


def get_plist_data(dict):
     data = {}
     for index,item in enumerate(dict):
         if item.tag == "key":
             if dict[index+1].tag == "string":
                 data[item.text] = dict[index + 1].text
             if dict[index].text == "rotated":
                 data[item.text] = dict[index+1].tag
             if dict[index+1].tag == "dict":
                 data[item.text] = get_plist_data(dict[index+1])
     return data


def run(file_plist,file_png):
    save_path = file_plist.replace(".plist", "")
    png_image = Image.open(file_png)
    # dom解析plist文件信息
    dict = ElementTree.fromstring(open(file_plist, "r").read())
    plistInfo = get_plist_data(dict[0])
    print plistInfo

    to_list = lambda x: x.replace('{', '').replace('}', '').split(',')

    for k, v in plistInfo['frames'].items():
        if v.has_key('textureRect'):
            rectlist = to_list(v['textureRect'])
        elif v.has_key('frame'):
            rectlist = to_list(v['frame'])

        width = int(rectlist[2])
        height = int(rectlist[3])
        # if v.has_key('rotated'):
        #     width = int(rectlist[3] if v['rotated'] else rectlist[2])
        #     height = int(rectlist[2] if v['rotated'] else rectlist[3])
        # else:
        #     width = int(rectlist[2])
        #     height = int(rectlist[3])
        box = (
            int(rectlist[0]),
            int(rectlist[1]),
            int(rectlist[0]) + width,
            int(rectlist[1]) + height,
        )
        print rectlist
        print box
        print width
        print height
        print "================="
        # print v
        if v.has_key('spriteSize'):
            spriteSize = v['spriteSize']
        elif v.has_key('sourceSize'):
            spriteSize = v['sourceSize']

        sizelist = [int(x) for x in to_list(spriteSize)]
        # print sizelist
        rect_on_big = png_image.crop(box)

        if v['rotated'] == "true":
            print "fanzhuan---"
            rect_on_big = rect_on_big.rotate(90)

        result_image = Image.new('RGBA', sizelist, (0, 0, 0, 0))

        if (v.has_key('textureRotated') and v['textureRotated']) or (v.has_key('rotated') and v['rotated']):
            result_box = (
                (sizelist[0] - height) / 2,
                (sizelist[1] - width) / 2,
                (sizelist[0] + height) / 2,
                (sizelist[1] + width) / 2
            )
        else:
            result_box = (
                (sizelist[0] - width) / 2,
                (sizelist[1] - height) / 2,
                (sizelist[0] + width) / 2,
                (sizelist[1] + height) / 2
            )
        print result_box
        # result_image.paste(rect_on_big, result_box, mask=0)
        result_image.paste(rect_on_big)

        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        outfile = save_path + "\\" + k
        print outfile
        result_image.save(outfile)


def listdir(path,list_name):
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        if os.path.isdir(f):
            listdir(f,list_name)
        elif os.path.splitext(file_path)[1]=='.plist' or os.path.splitext(file_path)[1]=='.png':
            list_name.append(file_path)
    return list_name


if __name__ == "__main__":
    print "开始运行"
    # file_path = raw_input("请输入分解的plist文件的根路径:file_path=")
    file_plist = raw_input("请输入分解的plist文件的全路径:file_plist=")
    # file_plist = "C:\\Users\HP\\Desktop\\unpackerPlist\\unpack-plist\\number.plist"
    file_png = os.path.splitext(file_plist)[0] + ".png"
    if os.path.exists(file_plist) and os.path.exists(file_png):
        run(file_plist, file_png)
    else :
        print "please input a vaild path"

