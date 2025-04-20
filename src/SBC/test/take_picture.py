import cv2
import numpy as np

# GStreamer pipeline for capturing from the CSI camera
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
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

def capture_image():
    window_title = "CSI Camera - Capture Image"

    # Create a VideoCapture object using the GStreamer pipeline
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            print("Press 'c' to capture the image or 'q' to quit.")
            while True:
                ret_val, frame = video_capture.read()

                # Check to see if the user closed the window
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    # Display the frame for capturing
                    cv2.imshow(window_title, frame)
                else:
                    break

                # Capture image on 'c' key press
                keyCode = cv2.waitKey(10) & 0xFF
                if keyCode == ord('c'):
                    cv2.imwrite("picture.png", frame)  # Save the captured image
                    print("Image captured and saved as picture.png")
                    break
                elif keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    capture_image()
