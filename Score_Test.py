from PIL import Image
import os
import numpy as np
num=100
t_step = 1.0 / (num - 1)
t = np.arange(0.0,1+t_step,t_step)
print(t)
exit()

from sklearn.metrics.pairwise import cosine_similarity

def Check(my_folder,golden_folder):
    my_list = os.listdir(my_folder)
    my_list.sort()

    golden_list = os.listdir(golden_folder)
    golden_list.sort()

    if len(my_list)!=len(golden_list):
        print("Hit Bad Trap")
        exit()

    for i in range(len(my_list)):
        my_imurl = os.path.join(my_folder, my_list[i])
        go_imurl=os.path.join(golden_folder, my_list[i])
        myim = Image.open(my_imurl)
        myim_array = np.array(myim)

        goim = Image.open(go_imurl)
        goim_array = np.array(goim)


        diff=0
        total=0
        empty=np.array([255,255,255])



        for (q, j) in zip(myim_array, goim_array):
            for (k,l) in zip(q,j):

                c = (k == l)
                if (empty == k).all():
                    pass
                else:
                    total += 1

                if c.all():
                    pass
                else:
                    diff+=1

                #print(k)

        print("Test At: ",my_list[i])
        print("With diff: ",100*diff/(total),"%     ",diff,"/",total)
        s = cosine_similarity(myim_array.reshape(1,-1), goim_array.reshape(1,-1))
        print("Cosine_similarity: ", s.flatten()[0])
        print("\n")
        #exit()
    #print("Hit Good Trap ~~~~~")

import sys
sys.path.insert(0, 'CG_DEMO')


import cg_cli
def Run():
    Check('img','goldimg')
    #Check('img', 'img')
Run()