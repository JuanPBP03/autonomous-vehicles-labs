import cv2
import numpy as np

# Function to calculate the average position of multiple detected line segments and draw a single representative line
def average_and_draw(lines, img, color):
    if len(lines) == 0:
        return
    x_coords, y_coords = [], []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        x_coords += [x1, x2]
        y_coords += [y1, y2]
    poly = np.polyfit(y_coords, x_coords, deg=1)
    y1 = img.shape[0]
    y2 = int(y1 * 0.45)
    x1 = int(np.polyval(poly, y1))
    x2 = int(np.polyval(poly, y2))
    cv2.line(img, (x1, y1), (x2, y2), color, 10)

# Open the video file for processing
vid = cv2.VideoCapture('test_video.mp4')

# Check if video file was successfully opened
if not vid.isOpened():
    print("Could not open video file")
else:
    print("Video file opened successfully")

# Video writer setup to save output video
fps = vid.get(cv2.CAP_PROP_FPS)
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('lane_detection_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Frame processing loop
while vid.isOpened():
    ret, frame = vid.read()
    if not ret:
        break

    # Image preprocessing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv2.Canny(blur, 50, 150)

    # Define ROI
    polygons = np.array([[
        (int(0.2 * width), height),
        (int(0.85 * width), height),
        (int(0.5 * width), int(0.45 * height)),
        (int(0.4 * width), int(0.45 * height))
    ]])
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, polygons, 255)
    roi = cv2.bitwise_and(edges, mask)

    # Detect lines with Hough Transform
    lines = cv2.HoughLinesP(roi, 1, np.pi / 180, 15, minLineLength=10, maxLineGap=150)

    # Classify lines into left and right lanes
    left_lines, right_lines = [], []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 - x1 == 0: continue
        slope = (y2 - y1) / (x2 - x1)
        if abs(slope) < 0.5: continue
        if slope < 0:
            left_lines.append(line)
        else:
            right_lines.append(line)

    # Draw average lines
    line_blank = np.zeros_like(frame)
    average_and_draw(left_lines, line_blank, (0, 255, 255))
    average_and_draw(right_lines, line_blank, (255, 0, 255))

    # Overlay lane lines onto original frame
    final = cv2.addWeighted(frame, 0.8, line_blank, 1, 1)
    out.write(final)

vid.release()
out.release()
cv2.destroyAllWindows()