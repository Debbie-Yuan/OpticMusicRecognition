import colorsys
import os

import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont
from tensorflow.keras.layers import Input, Lambda
from tensorflow.keras.models import Model

from models.nets.yolo4 import yolo_body, yolo_eval
from models.utils.utils import letterbox_image


class YOLO(object):
    _defaults = {
        "model_path": 'model_data/pic2sec.h5',
        "anchors_path": '/Users/daipeiyuan/developer/PyCharm/graduation_design'
                        '/models/yolov4_c/model_data/yolo_anchors.txt',
        "classes_path": 'model_data/sec_classes.txt',
        "score": 0.5,
        "iou": 0.3,
        "max_boxes": 100,
        "model_image_size": (416, 416),
        "letterbox_image": True,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    #   初始化yolo
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for k, v in kwargs.items():
            if self.__dict__.get(k) is not None:
                print(f'[YOLO CONFIG] Change value from old `{self.__dict__[k]}` to `{v}` from key `{k}`')
                self.__dict__[k] = v
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.generate()

    #   获得所有的分类
    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    #   获得所有的先验框
    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    #   载入模型
    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        #   计算先验框的数量和种类的数量
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)

        #   载入模型
        self.yolo_model = yolo_body(Input(shape=(None, None, 3)), num_anchors // 3, num_classes)
        self.yolo_model.load_weights(self.model_path)

        print('{} model, anchors, and classes loaded.'.format(model_path))

        # 画框设置不同的颜色
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))

        # 打乱颜色
        np.random.seed(10101)
        np.random.shuffle(self.colors)
        np.random.seed(None)

        #   在yolo_eval函数中，我们会对预测结果进行后处理
        #   后处理的内容包括，解码、非极大抑制、门限筛选等

        self.input_image_shape = Input([2, ], batch_size=1)
        inputs = [*self.yolo_model.output, self.input_image_shape]
        outputs = Lambda(yolo_eval, output_shape=(1,), name='yolo_eval',
                         arguments={'anchors': self.anchors, 'num_classes': len(self.class_names),
                                    'image_shape': self.model_image_size,
                                    'score_threshold': self.score, 'eager': True, 'max_boxes': self.max_boxes,
                                    'letterbox_image': self.letterbox_image})(inputs)
        self.yolo_model = Model([self.yolo_model.input, self.input_image_shape], outputs)

    @tf.function
    def get_pred(self, image_data, input_image_shape):
        out_boxes, out_scores, out_classes = self.yolo_model([image_data, input_image_shape], training=False)
        return out_boxes, out_scores, out_classes

    #   检测图片
    def detect_image(self, image, show_img=True):

        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        image = image.convert('RGB')

        #   给图像增加灰条，实现不失真的resize
        #   也可以直接resize进行识别
        if self.letterbox_image:
            boxed_image = letterbox_image(image, (self.model_image_size[1], self.model_image_size[0]))
        else:
            boxed_image = image.resize((self.model_image_size[1], self.model_image_size[0]), Image.BICUBIC)
        image_data = np.array(boxed_image, dtype='float32')
        image_data /= 255.

        #   添加上batch_size维度
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        #   将图像输入网络当中进行预测！
        input_image_shape = np.expand_dims(np.array([image.size[1], image.size[0]], dtype='float32'), 0)
        out_boxes, out_scores, out_classes = self.get_pred(image_data, input_image_shape)

        if show_img is False:
            return None, out_boxes, out_scores, out_classes

        #   设置字体
        font = ImageFont.truetype(
            font='/Users/daipeiyuan/developer/PyCharm/graduation_design/models/yolov4_c/font/simhei.ttf',
            size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = max((image.size[0] + image.size[1]) // 300, 1)

        for i, c in list(enumerate(out_classes)):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            top, left, bottom, right = box
            top = top - 5
            left = left - 5
            bottom = bottom + 5
            right = right + 5
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))

            # 画框框
            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)
            label = label.encode('utf-8')
            # print(label, top, left, bottom, right)

            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline=self.colors[c])
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=self.colors[c])
            draw.text(text_origin, str(label, 'UTF-8'), fill=(0, 0, 0), font=font)
            del draw

        return image, out_boxes, out_scores, out_classes
