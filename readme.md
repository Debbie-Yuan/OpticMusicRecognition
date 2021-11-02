# 多粒度光学乐谱识别系统

***

## 1. 系统需求

- `
  tensorflow~=2.2.0 numpy~=1.20.2  
  matplotlib~=3.4.1 Pillow~=8.1.2 PyQt5~=5.15.4 lxml~=4.6.3 labelImg~=1.8.4 setuptools~=54.2.0 pymusicxml==0.5.3 opencv-python==4.5.1.48 tqdm==4.60.0
  `


- Python版本需高于3.7.5

## 2. 辅助工具下载及链接

- 数据集下载 ： https://apacha.github.io/OMR-Datasets/
- MuseScore打谱软件下载：https://musescore.org/en
- LabelIMG：https://github.com/tzutalin/labelImg
- 作者标注的多粒度数据集及训练模型：
    - 链接： https://pan.baidu.com/s/13_mS9kjlhkdYKwN4xm4udw
    - 密码： ood2

## 3. 本项目使用的网络模型链接

- YOLOv4-tf2：https://github.com/bubbliiiing/yolov4-tf2

## 4. 本项目架构

- 如需启动项目，需要去网盘中下载作者训练的h5文件并放入models/yolov4_c/model_data文件夹下，保持文件名一致即可。

## 5. 结果及结果分析


## 6. 启动方式
- ``python Apps/base/main.py``
