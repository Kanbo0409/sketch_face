"""Utilities for measuring frame rate, and reading frames in a separate thread.

This code was mostly taken from: 
http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
"""

import cv2
import datetime
import time
from threading import Thread


class FPS:
    """Helper class to track number of frames and time elapsed."""

    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0
        self._last_update_time = time.time()

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1
        self._last_update_time = time.time()

    def elapsed_since_last_update(self):
        return (time.time() - self._last_update_time)

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval, or if that's missing, then till now
        end_time = self._end
        if not end_time:
            end_time = datetime.datetime.now()
        return (end_time - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()


class WebcamVideoStream:
    """Helper class that replaces the standard OpenCV usb camera reading methods, with a threaded version."""

    def __init__(self, src, width, height):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()

        if not self.grabbed:
            raise ValueError("Unable to read from camera device.")

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

            if not self.grabbed:
                raise ValueError("Unable to read from camera device.")

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
