# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    """
    Constructs a GStreamer pipeline string for use with OpenCV and the Jetson's CSI camera.

    Parameters:
        sensor_id      : ID of the CSI camera (usually 0 for default)
        capture_width  : Width of the camera capture
        capture_height : Height of the camera capture
        display_width  : Width of the display output
        display_height : Height of the display output
        framerate      : Frame rate of capture
        flip_method    : Flip method for camera image (0 = none)

    Notes:
        wbmode (White Balance Mode):
            0: Auto
            1: Incandescent
            2: Fluorescent
            3: Warm fluorescent
            4: Daylight
            5: Cloudy daylight
            6: Twilight
            7: Shade

        exposuremode (Exposure Mode):
            0: Auto
            1: Night
            2: Backlight
            3: Spotlight
            4: Sports
            5: Snow
            6: Beach
            7: Large aperture
            8: Very long
            9: Fixed FPS

        gaincontrol (Gain Control Mode):
            0: Auto
            1: Manual

    Returns:
        A formatted GStreamer pipeline string.
    """

    return (
        "nvarguscamerasrc sensor-id=%d wbmode=0 exposuremode=1 gaincontrol=0 ! "  # White Balance, Exposure, Gain
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "  # Ensure format is BGRx
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"  # Convert to BGR
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )



def show_camera():
    window_title = "CSI Camera"

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()
                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                else:
                    break 
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()
