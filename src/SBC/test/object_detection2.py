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
    """
    White Balance (wbmode):
        0: Auto, 1: Incandescent, 2: Fluorescent, 3: Warm fluorescent,
        4: Daylight, 5: Cloudy daylight, 6: Twilight, 7: Shade

    Exposure Mode (exposuremode):
        0: Auto, 1: Night, 2: Backlight, 3: Spotlight, 4: Sports,
        5: Snow, 6: Beach, 7: Large aperture, 8: Very long, 9: Fixed FPS

    Gain Control (gaincontrol):
        0: Auto, 1: Manual
    """
    return (
        "nvarguscamerasrc sensor-id=%d wbmode=4 exposuremode=1 gaincontrol=1 ! "
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

def detect_lines(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Orange
    lower_orange = np.array([160, 40, 180])
    upper_orange = np.array([180, 110, 255])

    # Blue
    lower_blue = np.array([100, 30, 60])
    upper_blue = np.array([135, 120, 160])

    # Masks
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find and draw orange contours
    contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_orange:
        if cv2.contourArea(contour) > 300:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 140, 255), 2)  # Orange-ish BGR
            cv2.putText(frame, "Orange Line", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 140, 255), 2)

    # Find and draw blue contours
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_blue:
        if cv2.contourArea(contour) > 300:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Blue Line", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return frame

def show_camera():
    window_title = "CSI Camera - Line Detection"

    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    if video_capture.isOpened():
        try:
            cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    frame = detect_lines(frame)
                    cv2.imshow(window_title, frame)
                else:
                    break

                if cv2.waitKey(10) & 0xFF in [27, ord('q')]:
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

if __name__ == "__main__":
    show_camera()
