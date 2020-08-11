#!/usr/bin/env python
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import math
from itertools import combinations, permutations

MIN_LINE_LENGTH = 30    #for hough transform
MAX_LINE_GAP = 40       #for hough transform
MIN_VOTES = 10         # for hough transform, represents minimum number of intersections to detect a line
NO_OF_SLOPE_BINS = 5         # for slope histogram
NO_OF_MIDPOINT_BINS = 3     #for midpoint abscissa histogram
DEPTH_MAX_RANGE = 10    # max range of the depth sensor
SLOPE_DIFF_THRESH = 10  # maximum difference in slope of lines to be merged, in degrees
LINE_PERP_DIST_THRESH =  20    # maximum perpendicular distance between lines to be merged
LINE_AX_DIST_THRESH =  40       # maximum axial distance between lines to be merged
DYNAMIC_RANGE = True


# returns perpendicular distance between two parallel lines
def perp_dist(l1, l2):
    m= (l1["slope"]  + l2["slope"])/2   # both slopes should almost be equal
    x_l1, y_l1 = l1["points"][0]
    x_l2, y_l2 = l2["points"][0]
    d = round(abs((y_l2 - y_l1) - m*(x_l2-x_l1))/math.sqrt(m**2 + 1))
    return d

#returns the distance between the closest coordinates of two lines
def axial_distance(l1, l2):
    res = midpoint_distance(l1, l2) - (line_length(l1)/2 + line_length(l2)/2)
    return abs(res)

# returns length of a line
def line_length(l):
    p1 = l["points"][0]
    p2 = l["points"][1]
    return point_dist(p1,p2)

# returns distance between the midpoints of two lines
def midpoint_distance(l1,l2):
    x1, y1 = l1["points"][0]
    x2, y2 = l1["points"][1]
    mp1 = ((x1+x2)/2,(y1+y2)/2)

    x1, y1 = l2["points"][0]
    x2, y2 = l2["points"][1]
    mp2 = ((x1+x2)/2,(y1+y2)/2)

    return point_dist(mp1,mp2)

# returns distance between two points
def point_dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)



def merge_lines(l1, l2):
    all_points = l1["points"] + l2["points"]
    enpoints=[]
    max_dist=-1
    for p1, p2 in permutations(all_points, 2):
        if point_dist(p1, p2) > max_dist:
            max_dist = point_dist(p1, p2)
            endpoints = [p1, p2]
    slope = (l1["slope"]  + l2["slope"])/2
    merged_line = {"points": endpoints, "slope": slope}
    # merged_line=l2
    # if line_length(l1)>line_length(l2):
    #     merged_line=l1
    return merged_line


bridge=CvBridge()

def ros_to_cv(data):
    try:
        img = bridge.imgmsg_to_cv2(data, "bgr8")
        return img

    except CvBridgeError as e:
        img = bridge.imgmsg_to_cv2(data)
        if data.encoding == "32FC1":
            min = 0
            max = DEPTH_MAX_RANGE
            if DYNAMIC_RANGE==True:
                min, max, _, _ = cv2.minMaxLoc(img)
            print("Minimum distance: ", min, "Maximum distance: ", max)
            mono_img = np.zeros(img.shape, np.uint8)
            cv2.convertScaleAbs(img,mono_img, 255.0/(max-min))
            img=mono_img
            return img

def edge_enhancement(img):
    scale = 1
    delta = 0
    ddepth = cv2.CV_16S

    dst = cv2.Sobel(img, ddepth, 0,1, ksize=5, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)

    abs_dst = cv2.convertScaleAbs(dst)
    check = cv2.convertScaleAbs(img+abs_dst)

    edges = cv2.Canny(check,30,200, apertureSize = 3)
    return edges


def callback(data):
    print()
    img = ros_to_cv(data)
    cv2.imshow('Video feed', img)
    edges = cv2.Canny(img,20,150, apertureSize = 3)
    # edges = edge_enhancement(img)
    cv2.imshow('Enhanced Edge Detection', edges)
    lines = cv2.HoughLinesP(edges,1,np.pi/180, MIN_VOTES, MIN_LINE_LENGTH, MAX_LINE_GAP)

    slope_set=[]
    slope_point_set=[]
    for line in lines:
        for x1,y1,x2,y2 in line:
            if x2-x1 != 0:
                slope = math.degrees(math.atan((y2-y1)/(x2-x1)))
            else:
                slope = 90
            slope_set.append(slope)
            slope_point_set.append({"points": [(x1,y1), (x2, y2)], "slope": slope})


    line_img = img.copy()
    for line in slope_point_set:
        x1,y1 = line["points"][0]
        x2,y2 = line["points"][1]
        cv2.line(line_img,(x1,y1),(x2,y2),(0),1)

    print("No. of lines before merging: ", len(slope_point_set))
    cv2.imshow('Hough lines output before merging', line_img)

    # merging lines with similar slope, less perpendicular distance and less axial distance
    i=0
    while(i<len(slope_point_set)-1):
        j=i+1
        while(j<len(slope_point_set)):
            line1 = slope_point_set[i]
            line2 = slope_point_set[j]
            slope1 = line1["slope"]
            slope2 = line2["slope"]
            pdist = perp_dist(line1,line2)
            adist = axial_distance(line1, line2)
            #print("Perpendicular distance: ", pdist)
            if abs(slope1 - slope2) <= SLOPE_DIFF_THRESH and pdist <= LINE_PERP_DIST_THRESH and adist <= LINE_AX_DIST_THRESH:

                # print("Lines to be merged: ", line1, line2)
                new_line = merge_lines(line1, line2)
                # print("Merged line: ", new_line)
                slope_point_set.pop(j)
                slope_point_set[i] = new_line
            j+=1
        i+=1

    print("No. of lines after merging: ", len(slope_point_set))
    #print("Set of lines after merging: ", slope_point_set)
    line_img_merged = img.copy()
    for line in slope_point_set:
        x1,y1 = line["points"][0]
        x2,y2 = line["points"][1]
        cv2.line(line_img_merged,(x1,y1),(x2,y2),(0),1)


    cv2.imshow('Hough lines output after merging', line_img_merged)

    slope_hist, slope_bin_edges = np.histogram(slope_set, NO_OF_SLOPE_BINS, (-45, 45))
    slope_mode_index = np.argmax(slope_hist)  # slope mode refers to slope of maximum frequency


    slope_lower_lim = slope_bin_edges [slope_mode_index]
    slope_upper_lim = slope_bin_edges [slope_mode_index+1]
    print("Slope limits: ", (slope_lower_lim, slope_upper_lim))

    midpoint_set=[]
    for line in slope_point_set:
        x1,y1 = line["points"][0]
        x2,y2 = line["points"][1]
        if x2-x1 != 0:
            slope = math.degrees(math.atan((y2-y1)/(x2-x1)))
        else:
            slope = 90

        if slope_lower_lim <= slope <= slope_upper_lim:
            midpoint_x = (x1+x2)/2
            midpoint_set.append(midpoint_x)

    midpoint_hist, midpoint_bin_edges = np.histogram(midpoint_set, NO_OF_MIDPOINT_BINS)
    midpoint_mode_index = np.argmax(midpoint_hist)  # midpoint mode refers to abscissa of maximum frequency

    midpoint_lower_lim = midpoint_bin_edges [midpoint_mode_index]
    midpoint_upper_lim = midpoint_bin_edges [midpoint_mode_index+1]
    print("Abscissa limits: ", (midpoint_lower_lim, midpoint_upper_lim))


    def midpoint_y(line):
        x1,y1 = line["points"][0]
        x2,y2 = line["points"][1]
        return (y1+y2)/2

    slope_point_set = sorted(slope_point_set, key = midpoint_y)


    midpoint_q = []

    for line in slope_point_set:
        x1,y1 = line["points"][0]
        x2,y2 = line["points"][1]
        if x2-x1 != 0:
            slope = math.degrees(math.atan((y2-y1)/(x2-x1)))
        else:
            slope = 90
        midpoint_x = (x1+x2)/2
        if slope_lower_lim <= slope <= slope_upper_lim and midpoint_lower_lim <= midpoint_x <= midpoint_upper_lim:
            cv2.line(img,(x1,y1),(x2,y2),(0),1)
            midpoint = (midpoint_x, (y1+y2)/2)
            midpoint_q.append(midpoint)
            if len(midpoint_q) == 2:
                cv2.line(img,midpoint_q[0],midpoint_q[1],(0),2)
                midpoint_q.pop(0)

    # Display the resulting frame
    cv2.imshow('Output', img)
    cv2.waitKey(2)

def listener():
    rospy.init_node('stair_detector', anonymous=True)
    rospy.Subscriber("/front_camera/depth/image_raw", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
