import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import mixed_precision



'''
first 4 numbers are the numbers that are being used
4th index [4] is addtion if 1 == True if 0 == False
[5] subtraction
[6] multiplication
[7] division
[8] parantheses
'''
A=11
S=12
M=13
D=14
P=15
NA=16
#1-10
problems_training_data=np.array([
[1,2,3,4,1,1,1,1,1],
[2,5,0,3,1,1,1,1,1],
[1,1,1,7,1,1,1,1,1],
[1,1,3,7,1,1,1,1,1],
[1,2,3,9,1,1,1,1,1],
[1,9,5,6,1,1,1,1,1],
[3,1,8,5,1,1,1,1,1],
[6,9,1,7,1,1,1,1,1],
[0,6,4,1,1,1,1,0,1],
[1,5,4,9,1,1,1,0,1],
[6,5,3,1,1,1,1,1,1],
[4,0,3,7,1,1,1,1,1],
[4,5,0,8,1,1,1,1,1],
[4,2,1,1,1,1,1,1,1],
[7,2,1,2,1,1,1,1,1],
[2,1,4,9,1,1,1,1,1],
[6,5,1,1,1,1,1,1,1],
[9,7,1,5,1,1,1,1,1],
[3,2,3,7,1,1,1,1,1],
[3,4,2,9,1,1,1,1,1],
[8,7,5,6,1,1,1,1,1],
[0,1,4,5,1,1,1,1,1],
[2,0,2,6,1,1,1,1,1],
[1,2,9,2,1,1,1,1,1],
[1,4,7,2,1,1,1,1,1],
[3,1,3,4,1,1,1,1,1],
##
[8,3,6,1,1,1,1,1,1],

            ])
#print(problems_training_data)
#1-10
solutions_traning_data=np.array([[0], [3], [1], [3], [4], [4], [9], [4], [1], [4], [4], [1], [9], [1], [5], [9], [4], [6], [9], [7], [9], [0], [0], [8], [5], [1], [6]

            ])

#11-15
checking_data_problems=np.array([
[1,2,1,8,1,1,1,1,1],
[1,3,2,5,1,1,1,1,1],
[1,7,8,9,1,1,1,1,1],
[6,3,0,7,1,1,1,1,1],
[4,1,2,8,1,1,1,1,1],
])


'''
A=add        +
S=subtract   -
M=multiply   *
D= division  /
P = Parantheses ()
NA means not used
number of posibale chocies, 16
len of a solution 			9
out put layer 144
'''



checking_data_solutions=np.array([
[3], [1], [4], [5], [4]

])
problems_training_data=problems_training_data.astype('float32')
solutions_traning_data=solutions_traning_data.astype('float32')
checking_data_problems=checking_data_problems.astype('float32')
checking_data_solutions=checking_data_solutions.astype('float32')


from keras.api._v2.keras import metrics


model = keras.Sequential([
    keras.Input(shape=(9)),
    layers.Dense(1024, activation = 'relu'),
    layers.Dense(512, activation = 'relu'),
    layers.Dense(256, activation = 'relu'),
    layers.Dense(10)
])

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.Adam(learning_rate=0.002),
    metrics=['accuracy'],
)


model.fit(problems_training_data,solutions_traning_data, batch_size=2, epochs=20, verbose=2)
model.evaluate(checking_data_problems,checking_data_solutions,batch_size=1,verbose=2)
