import xml.etree.ElementTree as EleT
from os import getcwd
from os.path import join

import cv2 as cv

from settings import CWD

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ['line', 'section', 'ts', 'G', 'F', 'C', '44', '24', '34', '38', '68', 'DC', 'DS', 'RJ', 'bpm']

wd = getcwd()


#
def convert_annotation(year_, image_id_, list_file_):
    in_file = open(join(wd, 'VOCdevkit/VOC%s/Annotations/%s.xml') % (year_, image_id_), encoding='utf-8')
    tree = EleT.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = 0
        if obj.find('difficult') != None:
            difficult = obj.find('difficult').text

        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text),
             int(xmlbox.find('ymax').text))
        list_file_.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


# 从标注中提取并导出
def extract_section(year_, image_id_):
    in_file = open(join(wd, 'VOCdevkit/VOC%s/Annotations/%s.xml') % (year_, image_id_), encoding='utf-8')
    tree = EleT.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        if obj.find('name').text == 'ts':
            xmlbox = obj.find('bndbox')
            # ymin:ymax, xmin:xmax
            b = (int(xmlbox.find('xmin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymin').text),
                 int(xmlbox.find('ymax').text))
            yield b


# 将标注转换为train， test文件
def process_annotation():
    for year, image_set in sets:
        image_ids = open(join(wd, 'VOCdevkit/VOC%s/ImageSets/Main/%s.txt') % (year, image_set)).read().strip().split()
        list_file = open('%s_%s.txt' % (year, image_set), 'w')
        for image_id in image_ids:
            list_file.write(join(wd, 'VOCdevkit/VOC%s/JPEGImages/%s.jpg') % (year, image_id))
            k = [b for b in extract_section(year, image_id)]
            # res_dict.setdefault(image_id, k)
            convert_annotation(year, image_id, list_file)
            list_file.write('\n')
        list_file.close()


# 将小节中的标注提取并转换为数据集
def process_sections():
    # 对于每一个数据集
    base_dir = "/Users/daipeiyuan/developer/PyCharm/graduation_design/data_set/ts"
    res_dict = {}
    for year, image_set in sets:
        # 获取到每一个图像
        image_ids = open(join(wd, f'VOCdevkit/VOC2007/ImageSets/Main/{image_set}.txt')).read().strip().split()
        for image_id in image_ids:
            # 将每一个id加入
            print(image_id)
            k = [b for b in extract_section(year, image_id)]
            res_dict.setdefault(image_id, k)
    # 提取每个文件
    for pic, pic_sections_locations in res_dict.items():
        # 首先打开这个文件
        fn = join(wd, f"VOCdevkit/VOC2007/JPEGImages/{pic}.jpg")
        img = cv.imread(fn)
        print(f"Opening fn : {fn}")
        for t, location in enumerate(pic_sections_locations):
            # ROI
            sec = img[location[2]:location[3], location[0]: location[1]]
            # 生成文件名
            sec_fn = f"{pic}@ts-{str(t)}.jpg"
            # 生成文件路径
            sec_pth = join(base_dir, sec_fn)
            print(f"Saving #{t}-{sec_pth}!")
            # 保存图像
            cv.imwrite(sec_pth, sec)


# 看图标注函数
def ann_ts():
    import os
    base = os.path.join(CWD, 'data_set/tss')
    images = open(os.path.join(base, 'anns.txt'), 'r').readlines()
    for image in images:
        ip = image.split(' ')[0]
        fn = ip.rstrip('\n')
        sfn = ip.split('/')[-1][-15:].rstrip('\n')
        img = cv.imread(fn)
        cv.imshow(sfn, img)
        cv.waitKey(0)
        cv.destroyAllWindows()


if __name__ == '__main__':
    # 当前使用处理标注并生成训练数据索引文件函数
    process_annotation()
