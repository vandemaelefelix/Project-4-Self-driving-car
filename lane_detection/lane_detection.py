# ---------------
# --- IMPORTS ---
# ---------------
import cv2 as cv
import numpy as np
import math
import time
from matplotlib import pyplot as plt

# -----------------
# --- VARIABLES ---
# -----------------
path = r'lane_detection/tape_images/image60.jpg'
img = cv.imread(path)
height, width, _ = img.shape
vertices = np.array([[0, height], [int(width/3), int(height/3)], [int((width/3)*2), int(height/3)], [width, height]])

# -----------------
# --- FUNCTIONS ---
# -----------------
def process_image(original_image):
    start_time = time.time()

    processed_image = original_image
    processed_image = cv.cvtColor(processed_image, cv.COLOR_BGR2GRAY)
    processed_image = cv.medianBlur(processed_image, 7)

    processed_image = cv.Canny(processed_image, threshold1=70, threshold2=150, apertureSize=3)
    processed_image = region_of_interest(processed_image, vertices)

    processed_image = cv.GaussianBlur(processed_image, (9, 9), sigmaX=0)

    lines = cv.HoughLinesP(processed_image, rho=1, theta=np.pi / 180, threshold=80, lines=100, minLineLength=10, maxLineGap=50)

    lane_lines = average_slope_intercept(processed_image, lines)
    draw_lines(original_image, lines, (0, 255, 0))
    draw_lines(original_image, lane_lines, (255, 255, 255))

    # draw_center_line(lane_lines)

    end_time = time.time()
    print('Processing took: {} seconds'.format(end_time - start_time))
    return original_image

def print_lines(lines):
    try:
        # print(lines_t[0])
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            # print('length: %s' % length)

    except:
        pass

def region_of_interest(image, vertices):
    mask = np.zeros_like(image)
    cv.fillPoly(mask, [vertices], 255)
    masked = cv.bitwise_and(image, mask)
    return masked

def draw_lines(image, lines, color):
    try:
        for line in lines:
            coords = line[0]
            cv.line(img=image, pt1=(coords[0], coords[1]), pt2=(coords[2], coords[3]), color=color, thickness=3, lineType=cv.LINE_AA)
    except:
        pass


# ------------------ EXPERIMENTAL ---------------------

def draw_center_line(line1, line2, coords1, coords2):
    m1, b1 = line1
    m2, b2 = line2
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    intersection = int(round(x)), int(round(y))
    x_coord2 = coords1[0][0]
    x_coord1 = coords2[0][0]
    print(x_coord1)
    print(x_coord2)
    mid_point = x_coord1 + (x_coord2 - x_coord1) / 2, height

    return [mid_point[0], mid_point[1], intersection[0], intersection[1]]

def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        print('No line_segment segments detected')
        return lane_lines

    height, width = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen
    print('left region boundary: %s' % left_region_boundary)
    print('right region boundary: %s' % right_region_boundary)
    print('Sum: {}'.format(left_region_boundary + right_region_boundary))

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                print('skipping vertical line segment (slope=inf): %s' % line_segment)
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1) # Vergelijking van een rechte creëeren y = mx + b
            slope = fit[0] # Helling => m
            intercept = fit[1] # Snijpunt met y-as => b
            if slope < 0: # Dalende lijn
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else: # Stijgende lijn
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    # Berekend de gemiddelde vergelijking van al de rechten in het linker segment
    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(left_fit_average))

    # Berekend de gemiddelde vergelijking van al de rechten in het rechter segment
    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(right_fit_average))

    print('lane lines: %s' % lane_lines)  # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]

    # print('centerline: %s' % draw_center_line(left_fit_average, right_fit_average, lane_lines[1], lane_lines[0]))

    # return draw_center_line(left_fit_average, right_fit_average, lane_lines[1], lane_lines[0])
    return lane_lines

# Converts polynomial (y = mx + b) to coördinates (x1, y1, x2, y2)
def make_points(line):
    slope, intercept = line
    y1 = height  # bottom of the frame
    # y2 = int(y1 * 1 / 2)  # make points from middle of the frame down
    y2 = 0  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

# -----------------------------------------------------

# ---------------------
# --- MAIN FUNCTION ---
# ---------------------
def main():
    cv.imshow('image', process_image(img))
    cv.waitKey(0)

if __name__ == "__main__":
    main()