

import tensorflow
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test)= mnist.load_data()
#print(y_train[0])

#for i in x_train[0]:
#  print(i)
x_train = x_train.reshape(-1,28*28).astype("float32")/255
x_test = x_test.reshape(-1, 28*28).astype("float32")/255
print(x_train.shape)
print(x_train[1].shape)


from keras.api._v2.keras import metrics
from keras.mixed_precision.loss_scale_optimizer import optimizer
model = keras.Sequential([
    keras.Input(shape=(784)),
    layers.Dense(512, activation = 'relu'),
    layers.Dense(256, activation = 'relu'),
    layers.Dense(10)
])

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    metrics=['accuracy'],
)

model.fit(x_train,y_train, batch_size=32, epochs=5, verbose=1)
model.evaluate(x_test,y_test,batch_size=32,verbose=2)
