# https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/
# first neural network with keras make predictions
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import confusion_matrix

# load the dataset
dataset = loadtxt('https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:, 0:8]
y = dataset[:, 8]
# define the keras model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu')) # https://keras.io/layers/core/
model.add(Dense(38, activation='relu'))
model.add(Dense(38, activation='relu'))
model.add(Dense(38, activation='tanh'))
model.add(Dense(38, activation='tanh'))
model.add(Dense(38, activation='tanh'))
model.add(Dense(1, activation='sigmoid'))
# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit the keras model on the dataset
model.fit(X, y, epochs=150, batch_size=1, verbose=1)
# make class predictions with the model
predictions = model.predict_classes(X)
# summarize the first 50 cases
for i in range(50):
    print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))

print('Confusion Matrix')
print(confusion_matrix(y, predictions))
