import PIL 
from PIL import Image
import os
import sys

def readf():
	
	try:
	    input_dir = str(sys.argv[1].rstrip('/'))
	    img_size = str(sys.argv[2])
	    output_dir = str(sys.argv[3].rstrip('/'))
	    print "Starting..."
	    print "Collecting data from %s" % input_dir
	    tclass = [d for d in os.listdir( input_dir )]
	    counter = 0
	    strdc = ''
	    hasil = []
	    for x in tclass:
		list_dir = os.path.join(input_dir,x)
		list_tuj = os.path.join(output_dir+'/', x+'/')
		if not os.path.exists(list_tuj):
			os.makedirs(list_tuj)
		if os.path.exists(list_tuj):
			for d in os.listdir(list_dir):
			    try:
				img = Image.open(os.path.join(input_dir+'/'+x,d))
				img = img.resize((int(img_size),int(img_size)),Image.ANTIALIAS)
				fname,extension = os.path.splitext(d)
				newfile = fname+extension
				if extension != ".png":
				#Uncomment to use .jpg				
				#if extension != ".jpg":
				   newfile = fname + ".png"
				   #Uncomment to use .jpg
				   #newfile = fname + ".jpg"
				#Uncomment to resize .png format
				img.save(os.path.join(output_dir+'/'+x,newfile))
				#Uncomment to resize .jpg format				
				#img.save(os.path.join(output_dir+'/'+x,newfile),"JPEG",quality=90)
				print "Resizing file : %s - %s" %(x,d)

			    except Exception,e:
				print "Error resize file : %s - %s" %(x,d)
				sys.exit(1)
			
			counter +=1

	except Exception,e:
	    print "Error, check Input directory etc : ", e
	    sys.exit(1)

readf()
