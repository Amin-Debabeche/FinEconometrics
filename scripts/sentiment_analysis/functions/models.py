import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential,Model
from keras import layers
from keras import backend as K
import numpy as np
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

def build_tcn(X, n_layers, cnn_dropout_p, dense_dropout_p, activation, n_dense_layers, n_dense_neurons, batch_normalization, kernel_initializer,
                 batch_size, optimizer):
        
    """Builds and compiles a keras 1DCNN model
    
    Parameters
    ----------
    X : ndarray
        a numpy array of the features array
    y : ndarray
        a numpy array of the labels array, one-hot-encoded!
    n_layers : int
        an integer indicating the number of times to repeat the core layers of the models
    cnn_dropout_p : float
        a float indicating the dropout probaiblity following the convolutional layers
    dense_dropout_p : float
        a float indicating the dropout probability following the dense layers
    activation : str
        a string indicating the name of the activation function to use in the convolutions
    n_dense_layers : int
        an integer indicating the number of dense layers
    n_dense_neurons : int
        an integer indicating the number of neurons in each dense layer
    batch_normalization : bool
        a boolean indicating whether to normalize the batches
    batch_size : int
        an integer indicating the size of the batch
    optimizer: keras Optimizer object
        a keras Optimizer object to perform the optimization of the model
    
    Returns
    -------
    keras.Model
        a compiled keras model with the provided hyper-parameters
    """  

    convolutions = [4, 4, 8, 16]
    double_cnn_per_layer = False
    
    loss = keras.losses.BinaryCrossentropy(from_logits=False)
    metrics = ['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
            
    inputs = keras.layers.Input(X.shape[1:])

    o = keras.layers.Conv1D(4, kernel_size = 3, activation = activation, kernel_initializer = kernel_initializer)(inputs)
    o = keras.layers.MaxPooling1D(pool_size = 2)(o)

    for n_layer in range(n_layers):

        o = keras.layers.Dropout(cnn_dropout_p)(o) if cnn_dropout_p is not None else o
        o = keras.layers.Conv1D(convolutions[n_layer], kernel_size = 3, activation = activation, kernel_initializer = kernel_initializer)(o)
        o = layers.BatchNormalization()(o) if batch_normalization else o
        o = keras.layers.Conv1D(convolutions[n_layer], kernel_size = 3, activation = activation, kernel_initializer = kernel_initializer)(o) if double_cnn_per_layer else o
        o = keras.layers.MaxPooling1D(pool_size = 2)(o)

    o = keras.layers.Flatten()(o)
    o = keras.layers.Dropout(dense_dropout_p)(o) if dense_dropout_p is not None else o

    for n_dense_layer in range(n_dense_layers):
        o = layers.Dense(n_dense_neurons, activation = activation)(o)
        o = keras.layers.Dropout(dense_dropout_p)(o) if dense_dropout_p is not None else o
    
    # Output softmax of bins
    o = layers.Dense(2, activation='softmax')(o)

    model = keras.Model(inputs, o)

    for var in optimizer.variables():
        var.assign(tf.zeros_like(var))

    model.compile(optimizer = optimizer, loss = loss, metrics = metrics)

    return model
    
def build_lstm(X, n_layers, lstm_neurons, n_dense_neurons, dropout, batch_size, activation, kernel_initializer, optimizer):
    
    """Builds and compiles a keras 1DLSTM model
    
    Parameters
    ----------
    X : ndarray
        a numpy array of the features array
    y : ndarray
        a numpy array of the labels array, one-hot-encoded!
    n_layers : int
        an integer indicating the number of times to repeat the core layers of the models
    lstm_neurons : int
        an integer indicating the number of neurons in each lstm layer
    n_dense_neurons : int
        an integer indicating the number of neurons in each dense layer
    dropout : float
        a float indicating the dropout probability following the lstm layers
    batch_size : int
        an integer indicating the size of the batch
    optimizer: keras Optimizer object
        a keras Optimizer object to perform the optimization of the model
    
    Returns
    -------
    keras.Model
        a compiled keras model with the provided hyper-parameters
    """  
        
    loss = keras.losses.BinaryCrossentropy(from_logits=False)
    metrics = ['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    
    # Configuration for LSTM model to not crash
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)

    input_shape = (batch_size, X.shape[1], X.shape[2])

    model = keras.models.Sequential()

    for n in range(0, n_layers):

        if n == 0:
            if n_layers == 1: 
                model.add(keras.layers.LSTM(lstm_neurons, batch_input_shape=input_shape, kernel_initializer=kernel_initializer, return_sequences=True))
            else: 
                model.add(keras.layers.LSTM(lstm_neurons, batch_input_shape=input_shape, kernel_initializer=kernel_initializer, return_sequences=True))
        elif n < n_layers-1: 
            model.add(keras.layers.LSTM(lstm_neurons, kernel_initializer=kernel_initializer, return_sequences=True))
        elif n == n_layers-1:
            model.add(keras.layers.LSTM(lstm_neurons, kernel_initializer=kernel_initializer)) 

        if dropout != None: 
            model.add(keras.layers.Dropout(dropout))

    if n_dense_neurons is not None: model.add(keras.layers.Dense(n_dense_neurons, activation=activation))
        
    # Output softmax of bins
    model.add(keras.layers.Dense(2, activation='softmax'))

    for var in optimizer.variables():
        var.assign(tf.zeros_like(var))

    model.compile(optimizer = optimizer, loss = loss, metrics = metrics)
    model.summary()

    return model