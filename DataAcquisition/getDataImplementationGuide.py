from os import path
from capture_data_functions import get_data, create_folder, timestamp

#in_path= 'C:\\Users\\ppou\\Downloads\\gitclone\\sg_benchmark\\data\\input\\RGBD' 
in_path='C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\DataAcquisition\\filesaving'

#New Folder Creation
path = create_folder(in_path, 'CITA_timeframe')

#Save files in the created folder
get_data(path, 'no', 10)

#renames files in the path with their timestamp
timestamp(path, 'CITA_timeframe')


########## USE IT WITH ONE FUNCTION ##########
# from os import path
# from capture_data_functions import get_data, create_folder

# #Yota's path
# in_path='C:\\Users\\ppou\\Downloads\\gitclone\\sg_benchmark\\data\\input\\RGBD'

# #Jen's path
# #in_path = 'C:\\Users\\jejor\\LocalCode\\sg_benchmark\\data\\input\\RGBD'


# #New Folder Creation
# path = create_folder(in_path, '-ela')

# #Save files in the created folder
# # path: where to save the output
# # w: write 'color' for colored_depth / anything else for regular
# # maximum_hole_size: the bigger number-the better
# # filename: the name of the CSV file that will have the metadata of the images
# # fr_number: the numbers of the frame that we want
# # timeframe: how many seconds should wait for each capture
# get_data(path, 'no', 10, 'CITA', 3, 15)
