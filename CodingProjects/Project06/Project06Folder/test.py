'''
test.py
Roman Schiffino 151B Fall Semester
This is just a test file to make sure my class worked well.
'''
import graphics as gr
import display as d
import tkinter as tk
import sys as s
import math as m
import filters as f
from matrix import *

A = matData(3,3,[[1,2,3],[1,2,3],[1,2,3]])
B = matData(3,3,[[4,5,6],[4,5,6],[4,5,6]])
C = matData(3,3,[[7,8,9],[7,8,9],[7,8,9]])
D = matData(3,3,[[10,11,12],[10,11,12],[10,11,12]])

E = A.rAppend(B)
F = D.lAppend(C)
G = E.dAppend(F)
print(G)