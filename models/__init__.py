from settings import PIC_MODEL_PTH, PIC_CLASSES_PTH, SEC_MODEL_PTH, SEC_CLASSES_PTH
from .nets.yolo4 import yolo_body as yolo4c
from .vgg16_c.predict import VGGBackbone, CLS_NAME
from .yolov4_c.yolo import YOLO

SEC2TSParams = {
    "model_path": SEC_MODEL_PTH,
    "classes_path": SEC_CLASSES_PTH,
}

print('\t[GD Net Model] Loading Section to TS initial data....')
SEC2TSModel = YOLO(**SEC2TSParams)
print('\t[GD Net Model] Section to TS loaded!\n')

PIC2SECParams = {
    "model_path": PIC_MODEL_PTH,
    "classes_path": PIC_CLASSES_PTH,
}
print('\t[GD Net Model] Loading Pic to Section initial data....')
PIC2SECModel = YOLO(**PIC2SECParams)
print('\t[GD Net Model] Pic to Section loaded!\n')

print('\t[GD Net Model] Loading TS Recognition initial data....')
TSRec = VGGBackbone()
print('\t[GD Net Model] TS Recognition initial data loaded!\n')
