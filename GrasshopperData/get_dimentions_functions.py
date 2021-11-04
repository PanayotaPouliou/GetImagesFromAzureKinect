from PIL import Image
import math
import pandas as pd

def get_obj_dimentions(obj_coords, obj_rect):
    #Set the camera position to be the O(0,0,0) point
    uo = 1920/2
    vo = 1080/2

    #FOV (90, 59) given by the depth camera settings
    a = 90*math.pi/180
    b = 59*math.pi/180

    fx = uo / math.tan(a/2)
    fy = vo / math.tan(b/2)

    #Create lists to host the acquired values
    Z=[]
    height_Bbox = []
    width_Bbox = []

    for i in range(len(obj_coords)):
        seperate=obj_coords[i]
        seperate = seperate.replace('(', '')
        seperate = seperate.replace(')', '')
        sep = seperate.split(", ")
        Z.append(float(sep[2]))
        #print(Z)
        #print(type(Z[i]))


    for i in range(len(obj_rect)):
        seperate=obj_rect[i]
        seperate = seperate.replace('[', '')
        seperate = seperate.replace(']', '')
        sep = seperate.split(", ")
        #print(type(sep[1]))


        #Get the pixel coordinates of the points that we want to get their real world coords
        xa,ya= float(sep[1]),float(sep[0])
        xb,yb= float(sep[3]),float(sep[2])
        #print(xa,ya)

        #calculate real world coordinates of point A
        xas= xa - uo
        yas= xb -vo

        xA= (Z[i]*xas)/fx
        yA= -(Z[i]*yas)/fy
        #print(xA,yA)

        #calculate real world coordinates of point B
        xbs= xb -uo
        ybs= yb -vo

        xB= (Z[i]*xbs)/fx
        yB= -(Z[i]*ybs)/fy
        #print(xB,yB)

        #The final width and height
        w= abs(xB-xA)
        h= abs(yB-yA)

        #Put width and height in one array each
        width_Bbox.append(w)
        height_Bbox.append(h)

    return width_Bbox, height_Bbox


def extract_ooo(path, save):
    # Read dataset csv with the material column
    data = pd.read_csv(path)
    
    #Object_check = data // Extract and host all detected object that have 0,0,0 as coordinates
    df1 = data.loc[data['coordinates'] == '(0.0, -0.0, 0)']
    df2 = data.loc[data['coordinates'] == '(-0.0, 0.0, 0)']
    frames = [df1,df2]
    object_check = pd.concat(frames)

    object_check = object_check.sort_index(ascending=True)
    object_check = object_check.reset_index()

    object_check.drop(columns=['attr' ,'attr_conf', 'index'], inplace=True)
    #print(object_check)
    if save:
        #Save dataframe to csv
        object_check.to_csv("Grasshopper/removed_objects.csv", index=False)
    return object_check


def remove_ooo(data):
    data = data[data.coordinates != '(0.0, -0.0, 0)']
    data = data[data.coordinates != '(-0.0, 0.0, 0)']
    data = data[data.coordinates != '(0, 0, 0)']
    return data


def grasshopper_input(path, save, save_ooo):
    # Read dataset csv with the material column
    data = pd.read_csv(path)

    removed_obg=extract_ooo(path, save_ooo)
    #print(removed_obg)

    data.drop(columns=['#', 'conf', 'attr', 'center', 'attr_conf'], inplace=True)

    data=remove_ooo(data)
    #print(data)


    #Get the values of 
    obj_coords = data['coordinates'].values
    obj_rect = data['rect'].values

    width_Bbox,height_Bbox= get_obj_dimentions(obj_coords, obj_rect)

    data['Bbox width'] = width_Bbox
    data['Bbox height'] = height_Bbox

    data = data.sort_index(ascending=True)
    data = data.reset_index()

    data.drop(columns=['index', 'rect'], inplace=True)

    #print(data)

    if save:
        #Save dataframe to csv
        data.to_csv("GrasshopperData/grassInput.csv", index=False)

    return data