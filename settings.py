from os.path import dirname, join

# from models import yolo4c

CWD = dirname(__file__)
DATASET_PTH = join(join(CWD, 'data_set'), 'ds2_voc_fmt')
DATASET_SEC_PTH = join(join(CWD, 'data_set'), 'sections')
MODEL_PTH = join(CWD, 'models')
MXML_LIB_PTH = join(CWD, 'mxml')
TEMP = join(CWD, 'temp')

DEFAULT = {
    'data_loader': None,
    'class_file_name': 'class.txt',
    'using_gpu': False,
    'plot_with_matplotlib': True,
    'save_checkpoint': True,
    'save_log': True,
    'weight_path': join(join(CWD, 'models'), 'weights'),
    'nn_log_path': join(join(CWD, 'logs'), 'NN'),
    'web_log_path': join(join(CWD, 'logs'), 'web'),
    'log_level': 'Critical'
}

DEBUG = DEFAULT.copy()
DEBUG['log_level'] = 'Info'

print(DATASET_PTH)

# PREDICT_MODEL_PTH = 'model_data/pic2sec.h5'
# PREDICT_CLASSES_PTH = 'model_data/sec_classes.txt'

SEC_MODEL_PTH = '/Users/daipeiyuan/developer/PyCharm/graduation_design/models/yolov4_c/model_data/sec2ts.h5'
SEC_CLASSES_PTH = '/Users/daipeiyuan/developer/PyCharm/graduation_design/models/yolov4_c/model_data/ts_classes.txt'

PIC_MODEL_PTH = '/Users/daipeiyuan/developer/PyCharm/graduation_design/models/yolov4_c/model_data/pic2sec_transforming.h5'
PIC_CLASSES_PTH = '/Users/daipeiyuan/developer/PyCharm/graduation_design/models/yolov4_c/model_data/sec_classes.txt'

VGG_BATCH_SIZE = 16
VGG_CLASS_NUM = 32
VGG_CLS_PTH = join(join(join(CWD, 'data_set'), 'tss'), 'classes.txt')
VGG_ANN_PTH = join(join(join(CWD, 'data_set'), 'tss'), 'anns.txt')
