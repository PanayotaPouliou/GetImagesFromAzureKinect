import csv
import os
import os.path
import time
from PIL import Image


def create_MetaData(path, filename):

    newpath = path + '\\' + filename + '.csv'
    # open the file in the write mode
    f = open(newpath, 'w')

    # create the csv writer
    writer = csv.writer(f)

    head = ['file_name', 'width', 'height',
            'timestamp', 'format', 'f_description', 'file']

    # write a row to the csv file

    writer.writerow(head)

    # close the file
    # f.close()

    return f


def timestamp(f_path): 
    # Getting the path of the file
    #f_path = 'C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\filesaving'
    path_c = f_path + '\\color.jpg'
    path_d = f_path + '\\Smooth_mapped.png'


    # Obtaining the creation time (in seconds)
    # of the file/folder (datatype=int)
    t = os.path.getctime(path_c)
    t2 = os.path.getctime(path_d)


    # Converting the time to an epoch string
    # (the output timestamp string would
    # be recognizable by strptime() without
    # format quantifers)
    t_str = time.ctime(t)
    t_str2 = time.ctime(t2)
  
    # Converting the string to a time object
    t_obj = time.strptime(t_str)
    t_obj2 = time.strptime(t_str2)

    # Transforming the time object to a timestamp
    # of Year_Month_Day_Hour_Min_Sec : 20211104173745
    form_t = time.strftime("%Y%m%d%H%M%S", t_obj)
    form_t2 = time.strftime("%Y%m%d%H%M%S", t_obj2)
  
    # Renaming the filename to its timestamp plus RGB or D depending on the img type
    os.rename(
        path_c, os.path.split(path_c)[0] + '/' + 'RGB_' + form_t + os.path.splitext(path_c)[1])
    
    os.rename(
        path_d, os.path.split(path_d)[0] + '/' + 'D_' + form_t2 + os.path.splitext(path_d)[1])

    return form_t, form_t2