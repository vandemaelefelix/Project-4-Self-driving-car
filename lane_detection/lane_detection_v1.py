# ---------------
# --- IMPORTS ---
# ---------------
import cv2 as cv
import numpy as np
import math
import time
from matplotlib import pyplot as plt
import logging


# -----------------
# --- VARIABLES ---
# -----------------
path = r'blue_tape_images/felixvdm/image5.jpg'
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
    try:
        start_time = time.time()

        processed_image = original_image
        processed_image = cv.cvtColor(processed_image, cv.COLOR_BGR2HSV)
        
        lower_blue = np.array([60, 40, 40])
        upper_blue = np.array([150, 255, 255])
        processed_image = cv.inRange(processed_image, lower_blue, upper_blue)
        processed_image = cv.Canny(processed_image, 200, 400)

        processed_image = region_of_interest(processed_image, vertices)

        processed_image = cv.GaussianBlur(processed_image, (3, 3), sigmaX=0)
        lines = cv.HoughLinesP(processed_image, rho=1, theta=np.pi / 180, threshold=80, lines=100, minLineLength=10, maxLineGap=50)

        lane_lines = average_slope_intercept(processed_image, lines)

        print(lane_lines)
        draw_lines(original_image, lines, (0, 255, 0))
        draw_lines(original_image, lane_lines, (255, 255, 255))

        angle = get_angle(lane_lines[0], lane_lines[1], original_image)

        print('Angle: %s' % angle)

        end_time = time.time()
        print('Processing took: {} seconds'.format(end_time - start_time))

        return original_image

    except Exception as e:
        logging.error(e)
        return original_image

def region_of_interest(image, vertices):
    """ 
    This function sets a region of interest where the lanes could be found.
    """
    try:
        mask = np.zeros_like(image)
        cv.fillPoly(mask, [vertices], 255)
        masked = cv.bitwise_and(image, mask)
        return masked
    except Exception as e:
        logging.error(e)
        return image

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

def get_angle(line1, line2, img):
    """  
    Creates a line in the middle of the two lane lines and returns the angle of that line.
    """
    try:
        # Coords and polynomial function line 1
        x11, y11, x12, y12 = line1[0]
        poly1 = np.polyfit((x11, x12), (y11, y12), 1)

        # Coords and polynomial function line 2
        x21, y21, x22, y22 = line2[0]
        poly2 = np.polyfit((x21, x22), (y21, y22), 1)

        # Calculate intersection point from polynomial functions
        x_inter = (poly1[1]-poly2[1]) / (poly2[0]-poly1[0])
        y_inter = poly1[0] * x_inter + poly1[1]

        # Calculate angle of center line
        angle_radians = math.atan2(y_inter - height, x_inter - (x21 - (abs(x11 - x21)/2)))
        angle_degrees = math.degrees(angle_radians)

        l = [x_inter, y_inter, x21 - (abs(x11 - x21)/2), height]
        cv.line(img=img, pt1=(int(l[0]), int(l[1])), pt2=(int(l[2]), int(l[3])), color=(255, 0, 0), thickness=3, lineType=cv.LINE_AA)

        return abs(angle_degrees)

    except Exception as e:
        logging.error(e)
        return 0

def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    try:
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

        return lane_lines

    except Exception as e:
        logging.error(e)
        return [[0, 0, 0, 0], [0, 0, 0, 0]]

def make_points(line):
    """ 
    Converts polynomial function (y = mx + b) to coördinates (x1, y1, x2, y2)
    """
    try:
        slope, intercept = line
        y1 = height  # bottom of the frame
        y2 = 0  # make points from middle of the frame down

        # bound the coordinates within the frame
        x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
        x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))

        return [[x1, y1, x2, y2]]

    except Exception as e:
        logging.error(e)
        return [[0, 0, 0, 0]]


# ---------------------
# --- MAIN FUNCTION ---
# ---------------------
def main():
    cv.imshow('image', process_image(img))
    cv.waitKey(0)

if __name__ == "__main__":
    main()