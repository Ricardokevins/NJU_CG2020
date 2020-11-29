#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    #

    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                result.append((x0, y))
        else:
            k = (y1 - y0) / (x1 - x0)
            if abs(k)>1:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                x=x0
                for y in range(y0,y1+1):
                    result.append((int(x), y))
                    x += (1 / k)
            else:
                if x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                y=y0
                for x in range(x0,x1+1):
                    result.append((x, int(y)))
                    y += k
    elif algorithm == 'Bresenham':
        print("Hit")
        print(x0,y0,x1,y1)
        if x0 == x1:
            if y0<y1:
                for y in range(y0, y1 + 1):
                    result.append((x0, y))
            else:
                for y in range(y1, y0 + 1):
                    result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)

            if abs(k)<1:
                if k>0:
                    delta_x=x1-x0
                    delta_y=y1-y0

                    p0=2*delta_y-delta_x
                    for x in range(x0,x1+1):

                        if p0<0:
                            result.append((x,y0))
                            p0+=2*delta_y
                        else:
                            y0+=1
                            result.append((x,y0))
                            p0=p0+2*delta_y-2*delta_x
                else:
                    delta_x = x1 - x0
                    delta_y = y1 - y0
                    delta_y = -delta_y
                    p0 = 2 * delta_y - delta_x
                    for x in range(x0, x1 + 1):

                        if p0 < 0:
                            result.append((x, y0))
                            p0 += 2 * delta_y
                        else:
                            y0 -= 1
                            result.append((x, y0))
                            p0 = p0 + 2 * delta_y - 2 * delta_x
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                if k>0:
                    delta_x=x1-x0
                    delta_y=y1-y0
                    p0=2*delta_x-delta_y
                    for y in range(y0,y1+1):
                        if p0<0:
                            result.append((x0,y))
                            p0+=2*delta_x
                        else:
                            x0 += 1
                            result.append((x0,y))
                            p0=p0+2*delta_x-2*delta_y
                else:
                    delta_y = y1 - y0
                    delta_x = x1 - x0
                    delta_x = -delta_x
                    p0 = 2 * delta_x - delta_y
                    for y in range(y0, y1 + 1):
                        if p0 < 0:
                            result.append((x0, y))
                            p0 += 2 * delta_x
                        else:
                            x0 -= 1
                            result.append((x0, y))
                            p0 = p0 + 2 * delta_x - 2 * delta_y
    if len(result)!=0:
        #print(result)
        pass
    else:
        print("Hit Error!!!!!!!",algorithm)
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result

def draw_polygoning(p_list,algorithm):
    # original version will connect all node 
    # but it`s not correct in Drawing not finished
    result = []
    for i in range(1,len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result

def draw_ellipse(p_list):
    """
    绘制椭圆（采用中点圆生成算法）
    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    cen_x=int((x1+x0)/2)
    cen_y=int((y0+y1)/2)

    rx = int((abs(x1 - x0)) / 2)
    ry = int((abs(y1 - y0)) / 2)
    x=0
    y=ry
    p0=float(ry**2-rx**2*ry+rx**2/4)
    
    temp_result=[]
    temp_result.append((x,y))
    temp_result.append((-x,y))
    temp_result.append((x,-y))
    temp_result.append((-x,-y))

    while (ry**2*x<rx**2*y):
        temp_result.append((x,y))
        if p0<0:
            p0+=float(2*ry**2*x+3*y**2)       
        else:
            p0+=float(2*ry**2*x-2*rx**2*y+2*rx**2+3*ry**2)
            y = y - 1
        x += 1
    (x,y)=temp_result[-1]
    p0=float((ry**2)*(x+0.5)**2+(rx**2)*(y-1)**2-(rx**2)*(ry**2))
    # print(rx, ry)
    # print(temp_result)
    while y>0:
        temp_result.append((x, y))
        if p0>=0:
            p0+=float(-2*rx**2*y+3*rx**2)
        else:
            p0+=float(2*ry**2*x-2*rx**2*y+2*ry**2+3*rx**2)
            x+=1
        y-=1
    for i in temp_result:
        result.append((cen_x+i[0],cen_y+i[1]))
        result.append((cen_x+i[0],cen_y-i[1]))
        result.append((cen_x-i[0],cen_y+i[1]))
        result.append((cen_x-i[0],cen_y-i[1]))
    #print(rx,ry)
    #print(temp_result)
    return result

def get_bezier_point(t, step, control_point):
    while(step!=1):
        for i in range(0, step-1):
            x0,y0=control_point[i]
            x1,y1=control_point[i+1]
            x=float(x0*(1-t))+float(x1*t)
            y=float(y0*(1-t))+float(y1*t)
            control_point[i]=x,y
        step-=1
    return control_point[0]


def bezier(p_list):
    num=len(p_list)*5000
    dis=1/num
    result=[]
    index=0
    t_list=[]
    while index<=1:
        t_list.append(index)
        index+=dis
    length=len(p_list)
    for i in t_list:
        x,y=get_bezier_point(i,length, p_list)
        result.append((int(x+0.5),int(y+0.5)))

    return result


def deboox_cox(i, deg , t,knot):
    '''
    :param i=knot_i:
    :param k=knot_i+deg:
    :param t=t:
    :return:
    '''
    if deg == 0:
        if knot[i]<=t and t<=knot[i+1]:
            return 1
        else:
            return 0
    else:
        temp1=knot[i+deg]-knot[i]
        temp2=knot[i+deg+1]-knot[i+1]
        if temp1==0 and temp2==0:
            return 0
        if temp1==0:
            return (knot[i+deg+1]-t)/temp2*deboox_cox(i+1,deg-1,t,knot)
        if temp2==0:
            return (t-knot[i])/temp1*deboox_cox(i, deg-1 , t,knot)
        return (t-knot[i])/temp1*deboox_cox(i, deg-1 , t,knot)+(knot[i+deg+1]-t)/temp2*deboox_cox(i+1,deg-1,t,knot)

def b_spline(p_list):
    k = 3
    result=[]
    n = len(p_list)
    du = float(1 / 1000)


    num=n+k+1
    knot=[]

    for i in range(num):
        knot.append(0)

    for i in range(k+1):
        knot[i]=0
        knot[-i-1]=1


    step=n-k+1
    per_step=1/step

    cur=0
    for i in range(k+1,n):
        cur+=per_step
        knot[i]=cur


    index=0
    temp=[]
    for i in range(10001):
        temp.append(index)
        index+=1/10000

    for u in temp:
        x1, y1 = 0, 0
        for i in range(0, n):
            x0, y0 = p_list[i]
            res = deboox_cox(i, k , u,knot)
            x1 += x0 * res
            y1 += y0 * res
        result.append([round(x1), round(y1)])
        u += du
    return result

def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    if algorithm=="Bezier":
        #print("Bezier")
        return bezier(p_list)
    #print("Not hit")
    if algorithm=="B-spline":
        #print("B-spline")
        return b_spline(p_list)
    else:
        print("Not implement")
        return 0

def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for i in p_list:
        i[0]+=dx
        i[1]+=dy
    return p_list


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    r/=180
    r*=math.pi

    cos_val=math.cos(r)
    sin_val = math.sin(r)

    for i in p_list:
        x_0 = i[0] - x
        y_0 = i[1] - y
        i[0]=int(x_0*cos_val-y_0*sin_val)+x
        i[1]=int(x_0*sin_val+y_0*cos_val)+y

    return p_list

def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """

    s=float(s)
    for i in p_list:
        x_0 = i[0] - x
        y_0 = i[1] - y
        i[0] = int(x_0 * s) + x
        i[1] = int(y_0 * s) + y

    return p_list


class CohenSutherland:
    def __init__(self,x_min, y_min, x_max, y_max):
        self.x_min=x_min
        self.y_min=y_min
        self.x_max=x_max
        self.y_max=y_max

    def encoder(self,x,y):
        c = 0
        if x < self.x_min:
            c = c | 1
        if x > self.x_max:
            c = c | 2
        if y < self.y_min:
            c = c | 4
        if y > self.y_max:
            c = c | 8
        return c

    def solve(self,p_list):
        x0, y0 = p_list[0]
        x1, y1 = p_list[1]
        code0=self.encoder(x0,y0)
        code1=self.encoder(x1,y1)
        outnode=code0
        x=0
        y=0

        while True:
            if code0 | code1==0:
                return [[x0,y0],[x1,y1]]
            if code0 & code1!=0:
                return []
            if code0==0:
                outnode=code1
            if 1 & outnode!=0:
                x = self.x_min
                y = y0 + (y1 - y0) * (self.x_min - x0) / (x1 - x0)
            elif 2 & outnode!=0:
                x = self.x_max
                y = y0 + (y1 - y0) * (self.x_max - x0) / (x1 - x0)
            elif 4 & outnode!=0:
                y= self.y_min
                x = x0 + ( x1 - x0) * (self.y_min - y0) / (y1 - y0)
            elif 8 & outnode!=0:
                y = self.y_max
                x = x0 + (x1 - x0) * (self.y_max - y0) / (y1 - y0)
            x=int(x)
            y=int(y)
            if outnode==code0:
                x0=x
                y0=y
                code0=self.encoder(x0,y0)
            else:
                x1=x
                y1=y
                code1 = self.encoder(x1, y1)

def LiangBarsky(x1,y1,x2,y2,XL,YB, XR,YT):
    if x1-x2==0:
        if x1<XL or x1>XR:
            return []
        else:
            ymin=max(YB,min(y1,y2))
            ymax=min(YT,max(y1,y2))
            if ymin<=ymax:
                re_x1=int(x1)
                re_x2=int(x1)
                re_y1=int(ymin)
                re_y2=int(ymax)
                return [[re_x1,re_y1],[re_x2,re_y2]]
            else:
                return []
    elif y1-y2==0:
        if x1<XL or x1>XR:
            return []
        else:
            xmin=max(XL,min(x1,x2))
            xmax=min(XR,max(x1,x2))
            if xmin<=xmax:
                re_y1=int(y1)
                re_y2=int(y1)
                re_x1=int(xmin)
                re_x2=int(xmax)
                return [[re_x1, re_y1], [re_x2, re_y2]]
            else:
                return []
    else:
        p1 = -(x2 - x1)
        p2 = -p1
        p3 = -(y2 - y1)
        p4 = -p3

        q1 = x1 - XL
        q2 = XR - x1
        q3 = y1 - YB
        q4 = YT - y1

        u1 = q1 / p1
        u2 = q2 / p2
        u3 = q3 / p3
        u4 = q4 / p4

        if p1<0:
            if p3<0:
                umin = max(0, max(u1, u3))
                umax = min(1, min(u2, u4))
            else:
                umin = max(0, max(u1, u4))
                umax = min(1, min(u2, u3))
        else:
            if p3 < 0:
                umin = max(0, max(u2, u3))
                umax = min(1, min(u1, u4))
            else:
                umin = max(0, max(u2, u4))
                umax = min(1, min(u1, u3))
        if umin<=umax:
            re_x1 = int(x1 + umin * (x2 - x1))
            re_x2 = int(x1 + umax * (x2 - x1))
            re_y1 = int(y1 + umin * (y2 - y1))
            re_y2 = int(y1 + umax * (y2 - y1))
            return [[re_x1, re_y1], [re_x2, re_y2]]
        else:
            return []

def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    if algorithm=="Cohen-Sutherland":
        solver=CohenSutherland(x_min, y_min, x_max, y_max)
        result=solver.solve(p_list)
        return result
    else:
        if algorithm=="Liang-Barsky":
            print("sdas")
            result=LiangBarsky(p_list[0][0],p_list[0][1],p_list[1][0],p_list[1][1],x_min, y_min, x_max, y_max)
            print(result)
            return result
        else:
            print("Not implement")
            exit()
