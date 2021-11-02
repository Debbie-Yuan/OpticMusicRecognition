import numpy as np
from PIL import Image


def str_list_to_label(cls_list, num_classes):
    y_labels = np.zeros(shape=(1, num_classes))
    for i in cls_list:
        if i == '':
            continue
        y_labels[0, int(i)] = 1
    return y_labels


def resize_images_with_padding(img_array):
    iw, ih = img_array.size  # 原始图像的尺寸
    w, h = (224, 224)  # 目标图像的尺寸

    scale = min(w / iw, h / ih)  # 转换的最小比例

    # 保证长或宽，至少一个符合目标图像的尺寸 0.5保证四舍五入
    nw = int(iw * scale + 0.5)
    nh = int(ih * scale + 0.5)

    image = img_array.resize((nw, nh), Image.BICUBIC)  # 更改图像尺寸，双立法插值效果很好
    # image.show()
    new_image = Image.new('RGB', (224, 224), (128, 128, 128))  # 生成灰色图像
    # // 为整数除法，计算图像的位置
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为黑色的样式
    # new_image.show()

    return new_image


# 224 * 224
def generate_arrays_from_txt(idx_file_pth: str, batch_size: int, num_classes: int):
    with open(idx_file_pth, 'r') as f:
        while True:
            # 用于存储批次图像
            images = list()
            # 标签
            y_labels = np.zeros(shape=(batch_size, num_classes))
            # 循环变量
            c = 0

            while len(images) < batch_size:
                line = f.readline()
                # 如果已经读到文件结尾并且本批次还不够，就需要继续从文件头补全
                if not line:
                    f.seek(0)
                    line = f.readline()

                t_ = line.strip('\n').split(' ')
                image_pth, labs = t_[0], t_[1:]
                img = resize_images_with_padding(Image.open(image_pth))
                # 填充并展平
                img = np.array(img)
                lab = str_list_to_label(labs, num_classes)

                images.append(img)
                y_labels[c] = lab
                c += 1
            # 扩展为可识别的numpy格式
            res = np.ndarray(shape=(batch_size, 224, 224, 3), dtype=np.float32)
            for _i, c in enumerate(images):
                res[_i] = c / 255
            yield res, y_labels
