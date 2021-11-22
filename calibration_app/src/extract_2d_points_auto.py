import numpy as np 
import cv2 as cv
import os
actual_file_path = os.path.dirname(os.path.abspath(__file__))
def vector_mgnitud(va, vb):
    r = ((vb[0]-va[0])**2+(vb[1]-va[1])**2)**0.5
    return r

def triangle_edges(triangle):
    a = triangle[0][0]
    b = triangle[1][0]
    c = triangle[2][0]

    return (vector_mgnitud(a, b), vector_mgnitud(a, c), vector_mgnitud(b, c))

def find_triangle_points(gray):
    
    # setting threshold of gray image
    # _, threshold = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    # using a findContours() function
    
    
    imagem = cv.bitwise_not(gray)
    cc = cv.imread(f"{actual_file_path}/mask_gray.jpg", 0)
    t_image = (gray*cc) + imagem
    _, threshold = cv.threshold(t_image, 127, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(
        threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    i = 0
    # list for storing names of shapes
    contour_draw = []
    first_t = True
    variance = 0
    tr_points = []
    for num, contour in enumerate(contours):
        # here we are ignoring first counter because
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue
        # cv.approxPloyDP() function to approximate the shape
        approx = cv.approxPolyDP(
            contour, 0.01 * cv.arcLength(contour, True), True)

        # putting shape name at center of each shape
        if len(approx) == 3:
            if first_t:
                variance = np.var(triangle_edges(approx))
                first_t = False
                tr_points = approx
                contour_draw = contour
                continue
            if np.var(triangle_edges(approx)) < variance:
                contour_draw = contour
                variance = np.var(triangle_edges(approx))
                tr_points = approx
    return tr_points

def pre_process_img(frame, lower_color_bounds, upper_color_bounds):
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    mask = cv.inRange(frame,lower_color_bounds,upper_color_bounds )
    kernel = np.ones((5,5),np.uint8)
    opening_mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    return opening_mask


def find_pairs(points_t1, points_t2):

    pair_tp1 = []
    pair_tp2 = []
    for t1_p in points_t1:
        
        for t2_p in points_t2:
            
            ptx = [t1_p[0][0], t2_p[0][0]]
            pty = [t1_p[0][1], t2_p[0][1]]
            p_std_x = np.std(ptx)/np.mean(ptx)
            p_std_y = np.std(pty)/np.mean(pty)
            if p_std_x < 0.1 and p_std_y < 0.1:
                pair_tp1.append(t1_p)
                pair_tp2.append(t2_p)
       
    points_t1_set = set(tuple(map(tuple, np.squeeze(points_t1))))
    points_t2_set = set(tuple(map(tuple, np.squeeze(points_t2))))
    tp1_pair_set = set(tuple(map(tuple, np.squeeze(pair_tp1))))
    tp2_pair_set = set(tuple(map(tuple, np.squeeze(pair_tp2))))
    center_tp1 =tp1_pair_set.symmetric_difference(points_t1_set)
    center_tp2 = tp2_pair_set.symmetric_difference(points_t2_set)

    return (np.squeeze(pair_tp1), center_tp1), (np.squeeze(pair_tp2), center_tp2)


def find_intersectoins(m1, b1, m2, b2):
    x = (b2 - b1)/(m1 - m2)
    y = (m1 * x) + b1
    return x, y

def find_line(x1, y1, x2, y2):
    m = (y2 - y1)/(x2 - x1)
    b = y1 - (m * x1)
    return m, b






def get_board_corners(path, show_graph):
    frame = cv.imread(path)

    lower_color_bounds = (0, 0, 0)
    upper_color_bounds = (80,80,80)
    opening_mask = pre_process_img(frame, lower_color_bounds, upper_color_bounds)
    points_t1 = find_triangle_points(opening_mask)

    lower_color_bounds = (80, 80, 80)
    upper_color_bounds = (255,255,255)

    opening_mask = pre_process_img(frame, lower_color_bounds, upper_color_bounds)
    points_t2 = find_triangle_points(opening_mask)

    triangle_1, triangle_2 = find_pairs(points_t1, points_t2)
    t1_ms = []
    t1_bs = []
    t2_ms = []
    t2_bs = []
    for point_t1, point_t2 in zip(triangle_1[0], triangle_2[0]):
        center_t1 = list(triangle_1[1])[0]
        center_t2 = list(triangle_2[1])[0]
        m_, b_ = find_line(point_t1[0], point_t1[1], center_t1[0], center_t1[1])
        t1_ms.append(m_)
        t1_bs.append(b_)
        m_, b_ = find_line(point_t2[0], point_t2[1], center_t2[0], center_t2[1])
        t2_ms.append(m_)
        t2_bs.append(b_)
        frame = cv.circle(frame, (point_t1[0], point_t1[1]), radius=5, color=(0, 0, 255), thickness=7)
        frame = cv.circle(frame, (point_t2[0], point_t2[1]), radius=5, color=(0, 255, 0), thickness=7)
        frame = cv.circle(frame, (center_t1[0], center_t1[1]), radius=5, color=(255, 0, 0), thickness=7)
        frame = cv.circle(frame, (center_t2[0], center_t2[1]), radius=5, color=(255, 255, 0), thickness=7)
    p1 = find_intersectoins(t1_ms[0], t1_bs[0], t1_ms[1], t1_bs[1])
    p2 = find_intersectoins(t2_ms[0], t2_bs[0], t2_ms[1], t2_bs[1])
    p3 = find_intersectoins(t1_ms[1], t1_bs[1], t2_ms[1], t2_bs[1])
    p4 = find_intersectoins(t1_ms[0], t1_bs[0], t2_ms[0], t2_bs[0])

    p1 = [int(i) for i in p1]
    p2 = [int(i) for i in p2]
    p3 = [int(i) for i in p3]
    p4 = [int(i) for i in p4]
    k_points = [p1,p2, p3, p4]
    k_points.sort()
    if show_graph:
        frame = cv.circle(frame, p1, radius=5, color=(0, 255, 255), thickness=5)
        frame = cv.circle(frame, p2, radius=5, color=(0, 255, 255), thickness=5)
        frame = cv.circle(frame, p3, radius=5, color=(0, 255, 255), thickness=5)
        frame = cv.circle(frame, p4, radius=5, color=(0, 255, 255), thickness=5)
        while(True):
            cv.imshow(path.split("/")[-1], frame)
            if cv.waitKey(20) & 0xFF == ord('q'):
                break
        cv.destroyAllWindows()
    return k_points
