import pathlib
import tensorflow as tf
import numpy as np
import copy
import cv2 as cv
import os

# vgg_16_model = tf.keras.models.load_model('main/vgg16_final/my_model')
# vgg_19_model = tf.keras.models.load_model('main/test2')
vgg_19_model_chess = tf.keras.models.load_model('kluiUI/model/test4_Chess')
vgg_19_model_color = tf.keras.models.load_model('kluiUI/model/test_color')
# cnn_model = tf.keras.models.load_model('main/cnn_final/my_model')

def get_board_vgg_19_edged():
    root = "kluiUI/klui_tempbox"
    data_dir = pathlib.Path(root)
    test_img=tf.keras.preprocessing.image_dataset_from_directory(data_dir,color_mode='rgb',image_size=(224, 224),shuffle=False,batch_size=32)
    predictions = np.array([])
    labels =  np.array([])
    for x, y in test_img:
      predictions = np.concatenate([predictions, np.argmax(vgg_19_model_chess.predict(x), axis=-1)])
      #labels = np.concatenate([labels, np.argmax(y.numpy(), axis=-1)])
    boards=predictions.reshape(8,8)
    return boards

def get_board_vgg_19_color():
    root = "kluiUI/klui_tempbox"
    data_dir = pathlib.Path(root)
    test_img=tf.keras.preprocessing.image_dataset_from_directory(data_dir,color_mode='rgb',image_size=(224, 224),shuffle=False,batch_size=32)
    predictions = np.array([])
    labels =  np.array([])
    for x, y in test_img:
      predictions = np.concatenate([predictions, np.argmax(vgg_19_model_color.predict(x), axis=-1)])
      #labels = np.concatenate([labels, np.argmax(y.numpy(), axis=-1)])
    boards=predictions.reshape(8,8)
    return boards

def predict_encode(boardss) :
    # Class=['bB','bK','bN','bQ','bR','--','bp','wB','wK','wN','wQ','wR','wp']
    Class=['B','K','N','Q','R','-','p']
    chess_board=np.zeros(shape=(8,8),dtype=object)
    for i in range(8) :
        for j in range(8) :
            chess_board[i][j] = Class[int(boardss[i][j])]
    return chess_board

def predict_color(boardss) :
    # Class=['bB','bK','bN','bQ','bR','--','bp','wB','wK','wN','wQ','wR','wp']
    Class=['b','-','w']
    chess_board=np.zeros(shape=(8,8),dtype=object)
    for i in range(8) :
        for j in range(8) :
            chess_board[i][j] = Class[int(boardss[i][j])]
    return chess_board

def combine(boardcolor, boardchess):
    chess_board = boardcolor
    for i in range(8) :
        for j in range(8) :
            chess_board[i][j] = boardcolor[i][j]+boardchess[i][j]
    return chess_board

def chesstrack(prevboaed,board):
    newboard = board
    missingpiece_position = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == prevboaed[i][j][0]:
                newboard[i][j] = newboard[i][j] + prevboaed[i][j][1]
            elif (board[i][j] != prevboaed[i][j][0]) and (prevboaed[i][j][0]=='-'):
                newpiece_position = (i,j)
            elif (board[i][j] != prevboaed[i][j][0]) and (prevboaed[i][j][0]!='-'):
                missingpiece_position = (i,j)
    newboard[newpiece_position[0]][newpiece_position[1]] = prevboaed[missingpiece_position[0]][missingpiece_position[1]]
    newboard[missingpiece_position[0]][missingpiece_position[1]] = prevboaed[newpiece_position[0]][newpiece_position[1]]
    return newboard

# boardchess = get_board_vgg_19_edged()
# print(boardchess)
# boardchess = predict_encode(boardchess)
# print(boardchess)

# boardcolor = get_board_vgg_19_color()
# print(boardcolor)
# boardcolor = predict_color(boardcolor)
# print(boardcolor)

# print(combine(boardcolor, boardchess))