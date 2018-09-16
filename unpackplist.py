# -*- coding: utf-8 -*-
import os, sys
from xml.etree import ElementTree
from PIL import Image

"""
获取图片的具体数据
plist 文件的大致结构是这样：
	<dict>
		<key>frames</key>
		<dict>
			<key>daoju/daoju051.png</key>
			<dict>
				<key>width</key>
				<integer>69</integer>
				<key>height</key>
				<integer>93</integer>
				  ......
			</dict>
			
			这是老版的TexturePacker 打包的plist格式
			新版需要重新修改 TODO
			因目前需求 需要解析老版，就先按老版的格式来解析
"""


def getImageData(dict):
    data = {}
    for index, item in enumerate(dict):
        if item.tag == "key":
            if dict[index + 1].tag == "string":
                data[item.text] = dict[index + 1].text
            elif dict[index + 1].tag == "integer":
                data[item.text] = dict[index + 1].text
            elif dict[index + 1].tag == "real":
                data[item.text] = dict[index + 1].text
            elif dict[index + 1].tag == "dict":
                data[item.text] = getImageData(dict[index + 1])
    return data


"""
dom 解析 ，先解析dict
再收取内层图片信息，通过Image模块保存单张图片
"""


def UnpackPngPlist(plist_fileName, png_fileName):
    save_file_path = plist_fileName.replace(".plist", "")
    all_image = Image.open(png_fileName)
    # dom解析plist文件信息
    dict = ElementTree.fromstring(open(plist_fileName, "r").read())
    plistInfo = getImageData(dict[0])

    for k, v in plistInfo["frames"].items():
        print v
        width = int(v["width"])
        height = int(v["height"])
        x = int(v["x"])
        y = int(v["y"])
        rect = (
            x,
            y,
            x + width,
            y + height,
        )
        sizelist = [width, height]
        print rect
        rect_on_big = all_image.crop(rect)

        result_image = Image.new('RGBA', sizelist, (0, 0, 0, 0))

        ##这个应该是计算锚点 的
        # result_box = (
        #     (x - width) / 2,
        #     (y - height) / 2,
        #     (x + width) / 2,
        #     (y + height) / 2
        # )
        # result_image.paste(rect_on_big, result_box, mask=0)
        result_image.paste(rect_on_big)

        # 老版可能存在多级路径
        pathList = k.split("/")
        print list
        path = ""
        extension = ""
        for pathStr in pathList:
            if ".png" not in pathStr:
                path += pathStr
            else:
                extension = pathStr

        path = save_file_path + "/" + path
        if not os.path.isdir(path):
            os.makedirs(path)
        outfile = (path + '/' + extension)
        print outfile, "generated"
        result_image.save(outfile)

if __name__ == '__main__':
    # fileName = sys.argv[1]
    # print fileName
    fileName = "number1"
    plist_fileName = fileName + ".plist"
    png_fileName = fileName + ".png"
    if (os.path.exists(plist_fileName) and os.path.exists(png_fileName)):
        UnpackPngPlist(plist_fileName, png_fileName)
    else:
        print "file path is not found"
