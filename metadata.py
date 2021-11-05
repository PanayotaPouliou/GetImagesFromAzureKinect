
from PIL import Image
#from PIL import ExifTags
from PIL.ExifTags import TAGS


# path to the image or video
imagename = "image.jpg"

# read the image data using PIL
image = Image.open(imagename)

# extract EXIF data
exifdata = image.getexif()
print(exifdata)

# iterating over all EXIF data fields
for tag_id in exifdata:
    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    # decode bytes 
    if isinstance(data, bytes):
        data = data.decode()
    print(f"{tag:25}: {data}")

#img = Image.open(r"DataAcquisition\filesaving\CITA\Smooth_mapped.png")
#print(img)

#exifdata = img.getexif()
#exif = { ExifTags.TAGS[k]: v for k, v in img.getexif() if k in ExifTags.TAGS }
#exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
#print(exifdata)





#Create a .txt file name to insert the image METADATA
#f= open("AcquireImageMetadata\imageMetadata.txt","w+")


#Write some lines in the .txt file 
#for i in range(10):
#    f.write("This is line %d\r\n" % (i+1))

#Open a created .txt file to append another image's METADATA
#f=open("AcquireImageMetadata\imageMetadata.txt", "a+")

#Append extra lines in the .txt file 
#for i in range(10):
#    f.write("Appended line %d\r\n" % (i+1))

#f.close()