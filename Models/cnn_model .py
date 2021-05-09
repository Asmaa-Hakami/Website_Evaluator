from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import cv2
import os
from sklearn.metrics import classification_report, confusion_matrix
from focal_loss import BinaryFocalLoss

train = ImageDataGenerator(rescale = 1/255)
train_dataset = train.flow_from_directory('/content/drive/MyDrive/WebImagesDataset/Train/',
                                          target_size = (200,200),
                                          batch_size = 32,
                                          class_mode = 'categorical')

test = ImageDataGenerator(rescale = 1/255)
test_dataset = train.flow_from_directory('/content/drive/MyDrive/WebImagesDataset/Test/',
                                          target_size = (200,200),
                                          batch_size = 32,
                                          class_mode = 'categorical')

model = tf.keras.models.Sequential([
                                    tf.keras.layers.Conv2D(16, (3,3), activation=tf.nn.relu,
                                    input_shape=(200, 200, 3)),
                                    tf.keras.layers.MaxPooling2D(2, 2),
                                    tf.keras.layers.Conv2D(32, (3,3), activation=tf.nn.relu),
                                    tf.keras.layers.MaxPooling2D(2, 2),
                                    tf.keras.layers.Conv2D(64, (3,3), activation=tf.nn.relu),
                                    tf.keras.layers.MaxPooling2D(2, 2),
                                    tf.keras.layers.Dropout(0.5),
                                    tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(250, activation=tf.nn.relu),
                                    tf.keras.layers.Dense(5,  activation=tf.nn.softmax)
                                    ])

model.compile(loss = BinaryFocalLoss(gamma=2), #'categorical_crossentropy',
              optimizer = 'adam', #RMSprop(lr = 0.001), # 'adam',
              metrics = ['accuracy'])

trf = model_fit = model.fit(train_dataset,
                      validation_data=test_dataset,
                      steps_per_epoch = len(train_dataset),
                      validation_steps=len(test_dataset),
                      epochs = 10)

Y_pred= model.predict(test_dataset)
y_pred = np.argmax(Y_pred, axis=1)
print(classification_report(test_dataset.classes, y_pred))

# accuracies
plt.plot(trf.history['accuracy'], label='train acc')
plt.plot(trf.history['val_accuracy'], label='test acc')
plt.legend()
plt.show()
