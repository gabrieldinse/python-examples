import numpy as np
import cv2
import turtle
import tensorflow as tf

def intersec(string1, string2):
    for letter in string1:
        if letter in string2:
            print(letter)

intersec('banana hahaha', 'mano que vc ta falando')