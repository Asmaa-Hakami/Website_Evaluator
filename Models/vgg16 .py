import tensorflow as tf
from tensorflow.keras import Sequential
from keras.layers import Input, Lambda, Conv2D, Flatten, Dense
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from keras.optimizers import SGD, Adam, Adagrad
from sklearn.metrics import classification_report, confusion_matrix
from focal_loss import SparseCategoricalFocalLoss

# re-size all the images to this
IMAGE_SIZE = [224, 224]

# add preprocessing layer to the front of VGG
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# don't train existing weights
for layer in vgg.layers:
  layer.trainable = False

# useful for getting number of classes
folders = glob('/content/drive/MyDrive/WebImagesDataset/Train/*')

# our layers - you can add more if you want
x = Flatten()(vgg.output)

#x = Dense(1000, activation='relu')(x)
prediction = Dense(len(folders), activation='softmax')(x)

# create a model object
model = Model(inputs=vgg.input, outputs=prediction)

# view the structure of the model
model.summary()

# tell the model what cost and optimization method to use
#opt = Adam(lr=0.0007, beta_1=0.9, beta_2=0.999, amsgrad=False)
model.compile(
  loss= tf.keras.losses.SparseCategoricalCrossentropy(), 
  optimizer='adam',
  metrics=['accuracy']
)

train_datagen = ImageDataGenerator(rescale = 1/255)

test_datagen = ImageDataGenerator(rescale = 1/255)

training_set = train_datagen.flow_from_directory('/content/drive/MyDrive/WebImagesDataset/Train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'sparse')

test_set = test_datagen.flow_from_directory('/content/drive/MyDrive/WebImagesDataset/Test',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'sparse') #categorical

# fit the model
r = model.fit(
  training_set,
  validation_data=test_set,
  epochs=10,
  steps_per_epoch= len(training_set),
  validation_steps=len(test_set)
)

# loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()

# accuracies
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='test acc')
plt.legend()
plt.show()

from keras.models import load_model

model.save('cnn.h5')

#Confusion Matrix and Classification Report
Y_pred = model.predict(test_set)
y_pred = np.argmax(Y_pred, axis=1)
#print('Confusion Matrix')
#print(confusion_matrix(test_set.classes, y_pred))
print('Classification Report')
#target_names = ['Bad', 'Excellent', 'Good','Very bad','Very good']
print(classification_report(test_set.classes, y_pred)) # target_names=target_names

from google.colab import drive
drive.mount('/content/drive')
