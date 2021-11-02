import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import SGD
from tensorflow.python.keras.optimizers import Adam

from models.nets.SmallVGGMultiLabel import SVML
from models.utils.vgg_utils import generate_arrays_from_txt
from settings import VGG_ANN_PTH, VGG_CLASS_NUM, VGG_BATCH_SIZE


def main():
    train_data_gen = generate_arrays_from_txt(VGG_ANN_PTH, VGG_BATCH_SIZE, VGG_CLASS_NUM)
    val_data_gen = generate_arrays_from_txt(VGG_ANN_PTH, VGG_BATCH_SIZE, VGG_CLASS_NUM)
    model = SVML(VGG_CLASS_NUM)
    sgd = SGD(lr=0.003, momentum=0.7, decay=0.01, nesterov=False)
    adam = Adam()
    model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
    tensor_board = TensorBoard()
    ckpt = ModelCheckpoint(
        'ts-cnn.h5',
        verbose=1,
        period=1,
        save_best_only=False
    )
    model.fit(train_data_gen,
              steps_per_epoch=32, epochs=25, verbose=1, callbacks=[tensor_board, ckpt],
              validation_data=val_data_gen, validation_steps=5)


if __name__ == '__main__':
    tf.compat.v1.disable_eager_execution()
    main()
