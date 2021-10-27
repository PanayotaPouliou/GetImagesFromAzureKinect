from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import csv
from depthFunctions_forVis import get_world_coord


df= pd.read_csv("CITAData.csv")
#print(df)


vals = df.values
#print(vals)

cita_list= vals.tolist()
#print(cita_list)

subj_centerx = df['subj_centerx'].to_list()
subj_centery = df['subj_centery'].to_list()
subj_depth = df['subj_depth'].tolist()
subj_id = df['subj_id'].tolist()

obj_centerx = df['obj_centerx'].tolist()
obj_centery = df['obj_centery'].tolist()
obj_depth = df['obj_depth'].tolist()
obj_id = df['obj_id'].tolist()

#create new csv with realworld coordinates
realCord = []
for i in range(len(subj_id)):
    sc=subj_centerx[i], subj_centery[i]
    sd=subj_depth[i]
    oc=obj_centerx[i], obj_centery[i]
    od=obj_depth[i]
    
    D, A, B = get_world_coord(sc, sd, oc, od)
    what = subj_id[i],A,obj_id[i],B
    realCord.append(what)

#print(realCord)

# field names 
fields = ['s_id', 'Xs,Ys,Zs', 'o_id', 'Xo,Yo,Zo'] 

with open('Subj-Obj_coords', 'w') as f:

    #using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(fields)
    write.writerows(realCord)