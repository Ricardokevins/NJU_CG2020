import matplotlib.pyplot as plt
import numpy as nmp
import math
#degree. 3次样条
knotType = 1   #knot的计算方式 0：平均取值  1：根据长度取值
CPointX = [235  ,385,  235  ,385  ]
CPointY = [173 , 223 , 273  ,323]
#控制轮廓顶点

# with open('data.txt', 'r') as f1:
#     list1 = f1.readlines()
#
# for i in range(len(list1)):
#     str = list1[i]
#     str1 = str.split(",")
#     CPointX.append(float(str1[0]))
#     CPointY.append(float(str1[1]))

n = len(CPointX)
knot = list(nmp.arange(n+3+1))
for i in range(0,4):
    knot[i] = 0.0
    knot[n+i] = 1.0

if knotType:
    L = list(nmp.arange(n-1))
    S = 0
    for i in range(n-1):
        L[i] = nmp.sqrt(pow(CPointX[i+1]- CPointX[i],2) + pow(CPointY[i+1]- CPointY[i],2))
        S = S + L[i]

    tmp = L[0]
    for i in range(4,n):
        tmp = tmp + L[i-3]
        knot[i] = tmp / S
else:
    tmp = 1 / (n-3)
    tmpS = tmp
    for i in range(4,n):
        knot[i] = tmpS
        tmpS = tmpS + tmp
print(knot)
#节点向量
#knot = [0,0,0,0,0.25,0.4,0.8,1,1,1,1]

def de_boor_cal(u,knot,X, Y):
    #判断u在哪个区间
    m = len(knot) #节点个数 且 m = n + k +1
    n = len(X)
    i = 3
    for i in range(3,m-3):
        if u>=knot[i] and u<knot[i+1]:
            break
    #递归计算
    if knot[i+3] - knot[i] == 0:
        a41 = 0
    else:
        a41 = (u - knot[i]) / (knot[i+3] - knot[i])
    if knot[i-1+3] - knot[i-1] == 0:
        a31 = 0
    else:
        a31 = (u - knot[i-1]) / (knot[i-1+3] - knot[i-1])
    if knot[i-2+3] - knot[i-2] == 0:
        a21 = 0
    else:
        a21 = (u - knot[i-2]) / (knot[i-2+3] - knot[i-2])

    XP40 = X[i]
    YP40 = Y[i]
    XP30 = X[i-1]
    YP30 = Y[i - 1]
    XP20 = X[i-2]
    YP20 = Y[i - 2]
    XP10 = X[i-3]
    YP10 = Y[i - 3]

    XP41 = (1 - a41) * XP30 + a41 * XP40
    YP41 = (1 - a41) * YP30 + a41 * YP40

    XP31 = (1 - a31) * XP20 + a31 * XP30
    YP31 = (1 - a31) * YP20 + a31 * YP30

    XP21 = (1 - a21) * XP10 + a21 * XP20
    YP21 = (1 - a21) * YP10 + a21 * YP20
    if knot[i+3-1] - knot[i] == 0:
        a42 = 0
    else:
        a42 = (u - knot[i]) / (knot[i+3-1] - knot[i])
    if knot[i-1+3-1] - knot[i-1] == 0:
        a32 = 0
    else:
        a32 = (u - knot[i-1]) / (knot[i-1+3-1] - knot[i-1])


    XP42 = (1 - a42) * XP31 + a42 * XP41
    YP42 = (1 - a42) * YP31 + a42 * YP41

    XP32 = (1 - a32) * XP21 + a32 * XP31
    YP32 = (1 - a32) * YP21 + a32 * YP31

    if knot[i+3-2] - knot[i] == 0:
        a43 = 0
    else:
        a43 = (u - knot[i]) / (knot[i+3-2] - knot[i])

    P43 = [(1 - a43) * XP32 + a43 * XP42,(1 - a43) * YP32 + a43 * YP42]
    return P43


plt.plot(CPointX,CPointY, '-ob', label="Waypoints")
plt.grid(True)
plt.legend()
plt.axis("equal")

Bspline = [[],[]]
for u in nmp.arange(0.0,1.0,0.0005):
    P = de_boor_cal(u,knot,CPointX,CPointY)
    Bspline[0].append(P[0])
    Bspline[1].append(P[1])

Bspline[0].append(CPointX[-1])
Bspline[1].append(CPointY[-1])
plt.plot(Bspline[0],Bspline[1], 'r')
plt.show()