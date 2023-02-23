import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os
import time
from multiprocessing.connection import wait
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
from operator import itemgetter

def auto_canny(image, sigma=0.33):
    """
    Canny edge detection with automatic thresholds.
    """
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = int(max(160, (1.0 - sigma) * v))
    upper = int(min(300, (1.0 + sigma) * v))
    edged = cv.Canny(image, lower, upper)
 
    # return the edged image
    return edged
def hough_line(edges, min_line_length=100, max_line_gap=10):
    lines = cv.HoughLines(edges, 1, np.pi / 180, 110, min_line_length, max_line_gap)
    lines = np.reshape(lines, (-1, 2))
    return lines

def reduce_line(lines):
    newlines=[]
    for rho, theta in lines:
        if (theta>0.52 and theta<1.04) or (theta>2.09 and theta<2.61) or (theta>3.66 and theta<4.18) or (theta>5.23 and theta<5.75):
            pass
        else:
            newlines.append([rho,theta])
    # print(np.array(newlines))
    # print(len(np.array(newlines)))
    return np.array(newlines)
def show_line(lines,image):
    for rho, theta in lines:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 4000*(-b))
            y1 = int(y0 + 4000*(a))
            x2 = int(x0 - 4000*(-b))
            y2 = int(y0 - 4000*(a))
            cv.line(image,(x1,y1),(x2,y2),(0,0,255),2)

def h_v_lines(lines):
    h_lines, v_lines = [], []
    for rho, theta in lines:
        if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
            v_lines.append([rho, theta])
        else:
            h_lines.append([rho, theta])
    return h_lines, v_lines

def intersections(h, v):
    """
    Given lists of horizontal and vertical lines in (rho, theta) form, returns list
    of (x, y) intersection points.
    """
    points = []
    for d1, a1 in h:
        for d2, a2 in v:
            A = np.array([[np.cos(a1), np.sin(a1)], [np.cos(a2), np.sin(a2)]])
            b = np.array([d1, d2])
            point = np.linalg.solve(A, b)
            points.append(point)
    return np.array(points)

def cluster_points(points):
    dists = spatial.distance.pdist(points)
    single_linkage = cluster.hierarchy.single(dists)
    flat_clusters = cluster.hierarchy.fcluster(single_linkage, 15, 'distance')
    cluster_dict = defaultdict(list)
    for i in range(len(flat_clusters)):
        cluster_dict[flat_clusters[i]].append(points[i])
    cluster_values = cluster_dict.values()
    clusters = map(lambda arr: (np.mean(np.array(arr)[:, 0]), np.mean(np.array(arr)[:, 1])), cluster_values)
    #for i in range(len(clusters)) :
        #clusters[i]=list(clusters[i])
        #a=clusters[i][0]
        #b=clusters[i][1]
        #clusters[i].append(cv.norm((int(a),int(b)),(0,int(b)), normType=cv.NORM_L2))
        #clusters[i]=tuple(clusters[i])
    return sorted(list(clusters), key=lambda k: [k[1],k[0]])

def clean_point(points):
    over_point=[]
    points=np.array(points,dtype=int)
    num_point=int(len(points))
    if num_point==90 or num_point==99:
        points=np.reshape(points,(int(num_point/9),9,2))
        for i in range(0,2) :
            #print(points[i][0][1],points[i+1][0][1])
            #if cv.norm(points[i][0],points[i+1][0], normType=cv.NORM_L2) <30 :
            if abs(points[i][0][1]-points[i+1][0][1])<30:
                over_point.append(i+1)
                print(over_point)
        for i in range(int(num_point/9)-1,int(num_point/9)-3,-1) :            
           # print(points[i][0][1],points[i-1][0][1])
            #if cv.norm(points[i][0],points[i-1][0], normType=cv.NORM_L2) <30 :
            if abs(points[i][0][1]-points[i-1][0][1])<30:
                over_point.append(i-1)
                print(over_point)
        x=0       
        for j in over_point :            
            points=np.delete(points,j-x,axis=0)
            x+=1
    elif num_point==81 :
        points=np.reshape(points,(int(len(points)/9),9,2))    
    else :
        print("error")
        print(num_point)
    temp = np.zeros(shape=(9,9,2),dtype=int)
    for i in range(0,9) :
        x=sorted(tuple(points[i]),key=itemgetter(0))
        for j in range(0,9) :
            temp[i][j]=x[j]
    return temp

def clean_point2(points):
    over_point=[]
    # points=np.array(points,dtype=int)
    num_point=len(points)
    print('num_point',num_point)
    # print(num_point,'p001',points.sort())
    if num_point==99:
        points = points[9:90]  
        points=np.array(points,dtype=int)
        # print('p1',points)
        points=np.reshape(points,(int(len(points)/9),9,2))
    else :
        print("error")
        print(num_point)
    # temp = np.zeros(shape=(9,9,2),dtype=int)
    # for i in range(0,9) :
    #     x=sorted(tuple(points[i]),key=itemgetter(0))
    #     for j in range(0,9) :
    #         temp[i][j]=x[j]
    # print('p0',points)
    # print('p0sort',points.sort())
    
    # print('p2',points)
    return points

def get_box(points,img):
    box=np.zeros(shape=(8,8,4,2),dtype=int)
    picture=np.float32([[0,0],[124,0],[124,124],[0,124]])
    for i in range(0,8) :
        for j in range(0,8) :
            box[i][j][0]=points[i][j]
            box[i][j][1]=points[i][j+1]
            box[i][j][2]=points[i+1][j+1]
            box[i][j][3]=points[i+1][j]
            #########ครอปภาพ
            my_box=np.float32([box[i][j][0],box[i][j][1],box[i][j][2],box[i][j][3]])
            my_picture=cv.getPerspectiveTransform(my_box,picture)
            img_output=cv.warpPerspective(img,my_picture,(124,124))
            #cv.imwrite(img_name+'_'+str(i)+str(j)+".png",img_output)
            path = 'main/klui_tempbox/img'
            cv.imwrite(os.path.join(path , str(i)+str(j)+'.png'),img_output)

def take_picture(port):
    cap = cv.VideoCapture(port,cv.CAP_DSHOW)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 900)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 900)
    w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    time.sleep(2) 
    ret, frame = cap.read()
    frame = frame[0:0+h, 100:100+730] 
    #frame=cv.imread("A1.jpg")
    (h,w) = frame.shape[:2]
    center = (w//2,h//2)
    M = cv.getRotationMatrix2D(center,0,1.0)
    rotated = cv.warpAffine(frame,M,(w,h),borderMode=cv.BORDER_REPLICATE)
    cap.release()
    cv.destroyAllWindows()
    rotated=cv.resize(rotated, (640,640))
    return rotated

"""
raw = take_picture(0)
# cv.imshow('frame',test)
# cv.waitKey(0)
img = raw

img_blur=cv.blur(img,(3,3),0)
gray_blur_kuy = cv.bilateralFilter(img, 9, 75, 75)
gray_blur_kuy = cv.medianBlur(gray_blur_kuy, 11)

# cv.imshow('blur', gray_blur_kuy)
# cv.waitKey(0)
# cv.destroyAllWindows()

mask=cv.subtract(img,gray_blur_kuy)
# cv.imshow('mask', mask)
# cv.waitKey(0)
# cv.destroyAllWindows()

final=cv.add(img_blur,1*mask)
# cv.imshow('final', final)
# cv.waitKey(0)
# cv.destroyAllWindows()

final = cv.cvtColor(final,cv.COLOR_BGR2GRAY)
cv.imshow('final2', final)
cv.waitKey(0)
cv.destroyAllWindows()

edges=auto_canny(final)
cv.imshow('edges', edges)
cv.waitKey(0)
cv.destroyAllWindows()

lines = hough_line(edges)
# print(lines)
# print(len(lines))
lines = reduce_line(lines)
liness=img.copy()
show_line(lines,liness)
cv.imshow('lines', liness)
cv.waitKey(0)
cv.destroyAllWindows()

h_lines, v_lines = h_v_lines(lines)
points = intersections(h_lines, v_lines )
points = cluster_points(points)
print('img shape',img.shape)
# print(len(points),points,(points[1][0],points[1][1]))
# img_copy = img
# for i in range(len(points)) :
#     cv.circle(img_copy,(int(points[i][0]),int(points[i][1])),5,(255, 0, 0),-1)
# cv.imshow('points', img_copy)
# cv.waitKey(0)
# cv.destroyAllWindows()
# cv.imshow('img', img)
# cv.waitKey(0)
# cv.destroyAllWindows()
img2=img

points=clean_point2(points)
print('shape point',points.shape)
# img_copy = img
# for i in range(len(points)) :
#     for j in range(len(points)) :
#         cv.circle(img_copy,(int(points[i][j][0]),int(points[i][j][1])),5,(0, 255, 0),-1)
# cv.imshow('points2', img_copy)
# cv.waitKey(0)
# cv.destroyAllWindows()

# box=get_box(points,img)
box=np.zeros(shape=(8,8,4,2),dtype=int)
# print(box)
# print(points)
# print('...........................................................')
testpoint = np.sort(points,axis=1)
print('shape testpoint',testpoint.shape)
# print(testpoint.sort(axis=1))
# print(points)
picture=np.float32([[0,0],[124,0],[124,124],[0,124]])
print('crop picture')
for i in range(0,8) :
    for j in range(0,8) :
        box[i][j][0]=testpoint[i][j]
        box[i][j][1]=testpoint[i][j+1]
        box[i][j][2]=testpoint[i+1][j+1]
        box[i][j][3]=testpoint[i+1][j]
        #########ครอปภาพ
        my_box=np.float32([box[i][j][0],box[i][j][1],box[i][j][2],box[i][j][3]])
        my_picture=cv.getPerspectiveTransform(my_box,picture)
        img_output=cv.warpPerspective(img2,my_picture,(124,124))
        #cv.imwrite(img_name+'_'+str(i)+str(j)+".png",img_output)
        # path = 'main/klui_crop_dataset1'
        path = 'kluiUI/klui_tempbox/img'
        # cv.imwrite(os.path.join(path , '30'+'_'+str(i)+str(j)+'.png'),img_output)
        cv.imwrite(os.path.join(path , str(i)+str(j)+'.png'),img_output)

"""




