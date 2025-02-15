from ultralytics import YOLO
from ultralytics.solutions import object_counter
import cv2

model = YOLO("yolov8n.pt")

# MP4 Capture
cap = cv2.VideoCapture("assets/video.mp4")

# Camera Capture
# cap = cv2.VideoCapture(0)


assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Define line points
line_points = [(20, 400), (1080, 400)]

# Video writer
video_writer = cv2.VideoWriter(
    "ml-video-output.avi",
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps,
    (w, h)
)

# Init Object Counter
counter = object_counter.ObjectCounter()
counter.set_args(
    view_img=True,
    view_in_counts=False,
    view_out_counts=False,
    reg_pts=line_points,
    classes_names=model.names,
    draw_tracks=True
)

classes_to_count = [0]

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    tracks = model.track(im0, persist=True, show=False, classes=classes_to_count)
    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()
