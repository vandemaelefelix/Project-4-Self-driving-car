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
path = r'./images/image60.jpg'
img = cv.imread(path)
height, width, _ = img.shape
vertices = np.array([[0, height], [int(width/3), int(height/3)], [int((width/3)*2), int(height/3)], [width, height]])

# -----------------
# --- FUNCTIONS ---
# -----------------
def process_image(original_image):
    """
    This function processes the image in several steps.
    (1) It makes the image gray.
    (2) It blurs the image.
    (3) It detects edges.
    (4) Sets a region of interest.
    (5) Detects lines in the image.
    (6) Detects the angle of the road.
    """
    start_time = time.time()

    processed_image = original_image
    processed_image = cv.cvtColor(processed_image, cv.COLOR_BGR2GRAY)
    processed_image = cv.medianBlur(processed_image, 7)

    processed_image = cv.Canny(processed_image, threshold1=70, threshold2=150, apertureSize=3)
    processed_image = region_of_interest(processed_image, vertices)

    processed_image = cv.GaussianBlur(processed_image, (9, 9), sigmaX=0)

    lines = cv.HoughLinesP(processed_image, rho=1, theta=np.pi / 180, threshold=80, lines=100, minLineLength=10, maxLineGap=50)

    lane_lines = average_slope_intercept(processed_image, lines)
    # draw_lines(original_image, lines, (0, 255, 0))
    draw_lines(original_image, lane_lines, (255, 255, 255))

    draw_center_line(original_image, lane_lines[0], lane_lines[1])

    end_time = time.time()
    print('Processing took: {} seconds'.format(end_time - start_time))
    return original_image


def region_of_interest(image, vertices):
    """ 
    This function sets a region of interest where the lanes could be found.
    """
    mask = np.zeros_like(image)
    cv.fillPoly(mask, [vertices], 255)
    masked = cv.bitwise_and(image, mask)
    return masked

def draw_lines(image, lines, color):
    """
    This function draws all lines in a list of lines on an image.
    """
    try:
        for line in lines:
            coords = line[0]
            cv.line(img=image, pt1=(coords[0], coords[1]), pt2=(coords[2], coords[3]), color=color, thickness=3, lineType=cv.LINE_AA)
    except:
        pass


# ------------------ EXPERIMENTAL ---------------------

def draw_center_line(img, line1, line2):
    l = intersection(line1, line2)
    cv.line(img=img, pt1=(int(l[0]), int(l[1])), pt2=(int(l[2]), int(l[3])), color=(255, 0, 0), thickness=3, lineType=cv.LINE_AA)
    print(intersection(line1, line2))

def intersection(line1, line2):
    # Coords line 1
    x11, y11, x12, y12 = line1[0]
    poly1 = np.polyfit((x11, x12), (y11, y12), 1)

    # Coords line 2
    x21, y21, x22, y22 = line2[0]
    poly2 = np.polyfit((x21, x22), (y21, y22), 1)

    # Calculate intersection point from polynomial functions
    x_inter = (poly1[1]-poly2[1]) / (poly2[0]-poly1[0])
    y_inter = poly1[0] * x_inter + poly1[1]

    return [x_inter, y_inter, abs(x11 - x21), height]

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

    print('lane lines: %s' % lane_lines)

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