# -*- coding: utf-8 -*-
import os,sys
from xml.etree import ElementTree
from PIL import Image


def get_plist_data(dict):
     data = {}
     for index,item in enumerate(dict):
         if item.tag == "key":
             if dict[index+1].tag == "string":
                 data[item.text] = dict[index + 1].text
             if dict[index].text == "offset":
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
    to_list = lambda x: x.replace('{', '').replace('}', '').split(',')
    for k, v in plistInfo['frames'].items():
        if v.has_key('frame'):
            rectlist = to_list(v['frame'])
        if v['rotated'] == "true":
            width = int(rectlist[3])
            height = int(rectlist[2])
        else:
            width = int(rectlist[2])
            height = int(rectlist[3])

        if v.has_key('offset'):
            offset = to_list(v['offset'])

        if v.has_key('sourceSize'):
            spriteSize = v['sourceSize']

        sizelist = [int(x) for x in to_list(spriteSize)]
        box = (
            int(rectlist[0]) + int(offset[0]),
            int(rectlist[1]) + int(offset[1]),
            int(rectlist[0]) + width,
            int(rectlist[1]) + height,
        )
        rect_on_big = png_image.crop(box)

        if v['rotated'] == "true":
            rect_on_big = rect_on_big.transpose(Image.ROTATE_90)

        result_image = Image.new('RGBA', sizelist, (0, 0, 0, 0))
        result_image.paste(rect_on_big, (0,0))

        outfile = save_path + os.sep + k
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        result_image.save(outfile)
        print outfile


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

