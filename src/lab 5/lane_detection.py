import cv2
import numpy as np

def average_and_draw(lines, img, color):
        if len(lines) == 0:
            return
        x_coords, y_coords = [], []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            x_coords += [x1, x2]
            y_coords += [y1, y2]
        poly = np.polyfit(y_coords, x_coords, deg=1)  # fit x = m*y + b
        y1 = img.shape[0]
        y2 = int(y1 * 0.45)
        x1 = int(np.polyval(poly, y1))
        x2 = int(np.polyval(poly, y2))
        cv2.line(img, (x1, y1), (x2, y2), color, 10)

vid = cv2.VideoCapture('test_video.mp4')

if not vid.isOpened():
    print("Could not open video file")
else:
    print("Video file opened successfully")

framenum = 1
# Get video properties
fps = vid.get(cv2.CAP_PROP_FPS)
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up video writer
out = cv2.VideoWriter(
    'lane_detection_output.mp4',
    cv2.VideoWriter_fourcc(*'mp4v'),  # Codec
    fps,
    (width, height)
)
while vid.isOpened():

    ret, frame = vid.read()
    if not ret:
        print('Frame ', framenum, 'failed to read or EOF')
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 50, 150)
    
    height, width = edges.shape

    polygons = np.array([
        [
            (int(0.2 * width), height),
            (int(0.85 * width), height),
            (int(0.5 * width), int(0.45 * height)),
            (int(0.4 * width), int(0.45 * height))
        ]
    ])
    
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, polygons, 255)
    roi = cv2.bitwise_and(edges, mask)

    lines = cv2.HoughLinesP(roi, 1, np.pi / 180, 15, minLineLength=10, maxLineGap=150)

    line_blank = np.zeros_like(frame)
    

    left_lines = []
    right_lines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 - x1 == 0:
            continue  # skip vertical lines
        slope = (y2 - y1) / (x2 - x1)
        if abs(slope) < 0.5:
            continue  # ignore near-horizontal lines
        if slope < 0:
            left_lines.append(line)
        else:
            right_lines.append(line)
    line_blank = np.zeros_like(frame)
    average_and_draw(left_lines, line_blank, (0, 255, 255))
    average_and_draw(right_lines, line_blank, (255, 0, 255))



    final = cv2.addWeighted(frame, 0.8, line_blank, 1, 1)
    out.write(final)  # Save current frame to video
    '''
    if framenum == 1:
        cv2.imshow('roi',roi)
        cv2.imshow('edges', edges)
        cv2.waitKey()
        cv2.destroyAllWindows()
    '''
    cv2.imshow('Lane Detection', final)
    

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    
vid.release()
out.release()
cv2.destroyAllWindows()
