
import pandas as pd
from get_dimentions_functions import grasshopper_input

path = r"GrasshopperData\Data\detections\detection_2021-11-01 14꞉03꞉53 c.jpg.csv"

data = grasshopper_input(path,save=True, save_ooo=False)
#print(data)