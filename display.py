""" Display conway's game of life """

import time

import cv2 # type: ignore
import numpy

import conway

DELAY = .125 # seconds
c = conway.Conway(rows=500, cols=500)

while True:
    cv2.imshow('frame', numpy.array(c.grid).astype(numpy.uint8) * 255)
    cv2.waitKey(1)
    time.sleep(DELAY)
    c.step()
