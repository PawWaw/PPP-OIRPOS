from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.applications.vgg19 import preprocess_input
from keras.applications.vgg19 import decode_predictions
from keras.applications.vgg19 import VGG19
from keras import models
from keras.layers import Flatten
from keras import layers
from keras.models import load_model
import tensorflow as tf

from tensorflow.compat.v1 import InteractiveSession

def runVGG19(path):
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)

    # załadowanie pretrenowanego modelu
    preTrainedModel = VGG19(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None)

    # wczytanie z pliku obrazu
    image = load_img('C:/Users/pawel/Desktop/border.jpg', target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    yhat = preTrainedModel.predict(image)

    label = decode_predictions(yhat)
    label = label[0][0]

    # wypisanie w konsoli klasyfikacji obrazu
    print('%s (%.2f%%)' % (label[1], label[2]*100))

    return label
# runVGG19('C:/Users/pawel/Desktop/border.jpg')