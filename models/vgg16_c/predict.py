import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

from models.utils.vgg_utils import resize_images_with_padding
from settings import VGG_BATCH_SIZE

CLS_NAME = [
    '下加3线-线上音符', '下加3线-上间音符', '下加2线-线上音符', '下加2线-上间音符', '下加1线-线上音符', '下加1线-上间音符', '1线-线上音符', '1线-上间音符', '2线-线上音符',
    '2线-上间音符', '3线-线上音符', '3线-上间音符', '4线-线上音符', '4线-上间音符', '5线-线上音符', '5线-上间音符', '上加一线-线上音符', '上加一线-上间音符', '上加二线-线上音符',
    '上加二线-上间音符', '上加三线-线上音符', '全音符', '二分音符', '四分音符', '八分音符', '十六分音符', '三十二分音符', '六十四分音符', '休止符', '附点符', '降音记号', '升音记号'
]

HDF5_PTH = '/Users/daipeiyuan/developer/PyCharm/graduation_design/models/vgg16_c/ts-cnn.h5'


def generate_predict_data(f_pth: str):
    # 处理图像
    img = resize_images_with_padding(Image.open(f_pth))
    # 生成数据
    test_data = np.zeros(shape=(VGG_BATCH_SIZE, 224, 224, 3), dtype=np.float32)
    # 填充数据
    test_data[0] = np.array(img) / 255

    return test_data


def predict(img_pth, f_pth=HDF5_PTH):
    # load
    model = load_model(f_pth)
    # summary
    model.summary()

    test_data = generate_predict_data(img_pth)

    pred = model.predict(test_data)
    return pred[0]


class VGGBackbone:

    def __init__(self):
        self.model = load_model(HDF5_PTH)
        print('\t[GD VGG] h5 file loaded!')
        self.door = 0.42

    @staticmethod
    def generate_predict_data(f_pth: str):
        # 处理图像
        img = resize_images_with_padding(Image.open(f_pth))
        # 生成数据
        test_data = np.zeros(shape=(VGG_BATCH_SIZE, 224, 224, 3), dtype=np.float32)
        # 填充数据
        test_data[0] = np.array(img) / 255

        return test_data

    def _map_to_output(self, vector, verbose, print_func):
        res = []
        cursor = 0
        if verbose:
            print_func("\t[GD VGG16 INNER] ", end_with_enter=False)
        for z, k in zip(CLS_NAME, list(vector)):
            if k > self.door:
                if verbose:
                    print_func(f"{z} - {k} ", end_with_enter=False)
                res.append(cursor)
            cursor += 1
        if verbose:
            print_func('\n', end_with_enter=False)
        return res

    def predict(self, image_pth, verbose=False, print_func=print):
        pred_data = self.generate_predict_data(image_pth)
        res = self.model.predict(pred_data)
        return list(res[0]), self._map_to_output(res[0], verbose, print_func)
