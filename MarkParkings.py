import numpy as np	
import cv2
from shapely.geometry import box, Polygon

def init():
	global i
	i=0
	global j
	j=0

#parkingsMarkedVar j
init()
j=0
# Check if the file TotalParkings.txt exists. If yes, get the total parkings or create new file and put the parkings as 1
try:
	fo = open('TotalParkings.txt','r')
except: # catch *all* exceptions
	j=1
if j==1:
	fo = open('TotalParkings.txt','w')
	fo.write(str(j-1))
	fo.close()
	
else:
	if j==0:
		j=1
	j=int(fo.readline(1))
	fo.close()
	#fo = open('TotalParkings.txt','w')
	#fo.write(str(j)+"\n")
	#fo.close()

pts=[0,1,2,3,4,5,6,7]

#img = cv2.imread('Car_Img.jpg')
img = cv2.imread('image5.jpg')
newx,newy = img.shape[1],img.shape[0]
img = cv2.resize(img,(newx,newy))
#width, height = cv.GetSize(src)    



def acccessI():
	print i

def drawParkings(j):
	polygon_shape = []
	parkingCoordinates=[0,1,2,3,4,5,6,7]
	countCoordinate=0
	#print j
	for parkingNum in range(1,j+1):
		print parkingNum
		with open('parking'+str(parkingNum)+'.txt') as masterData:
		#masterData=open('parking'+str(parkingNum)+'.txt','r')
			countCoordinate=0
			print parkingNum
			for line in masterData:
				if countCoordinate<=7:
					parkingCoordinates[countCoordinate]=int(line)
					print parkingCoordinates[countCoordinate]
					countCoordinate=countCoordinate+1
		
		#parkingCoordinates[1]=int(masterData.readline(2))
		#parkingCoordinates[2]=int(masterData.readline(3))
		#parkingCoordinates[3]=int(masterData.readline(4))
		#parkingCoordinates[4]=int(masterData.readline(5))
		#parkingCoordinates[5]=int(masterData.readline(6))
		#parkingCoordinates[6]=int(masterData.readline(7))
		#parkingCoordinates[7]=int(masterData.readline(8))
		pt = np.array([[parkingCoordinates[0],parkingCoordinates[1]],[parkingCoordinates[2],parkingCoordinates[3]],[parkingCoordinates[4],parkingCoordinates[5]],[parkingCoordinates[6],parkingCoordinates[7]]], np.int32)
		pt = pt.reshape((-1,1,2))
    		cv2.polylines(img,[pt],True,(255,0,0))
    		#xy=[[parkingCoordinates[0],parkingCoordinates[1]],[parkingCoordinates[2],parkingCoordinates[3]],[parkingCoordinates[4],parkingCoordinates[5]],[parkingCoordinates[6],parkingCoordinates[7]]
    		polygon_shape.append(Polygon(((parkingCoordinates[0],parkingCoordinates[1]),(parkingCoordinates[2],parkingCoordinates[3]),(parkingCoordinates[4],parkingCoordinates[5]),(parkingCoordinates[6],parkingCoordinates[7]))))
    	return polygon_shape

#Function to handle mouse clicks. Store the mouse clicks till it is the fourth. On fourth click draw the polygon and create new parking file.		
def mousePosition(event,x,y,flags,param):
	global i
	global j
	
	#Open parking file for the new Parking j that is to be marked	
	fo = open('parking'+str(j+1)+'.txt','a')
	if event == cv2.EVENT_LBUTTONDBLCLK:
		#printing the coordinates on the console
		print x,y
   		print i
   		pts[i]=x
   		pts[i+1]=y
   		i=i+2
   		#writing x,y coordinates in the file
   		fo.write(str(x)+"\n")
   		fo.write(str(y)+"\n")
		#cv2.line(img,(0,0),(511,511),(255,0,0),5)
		
		#When i=8 then the polygon is formed. Draw the same and open the next parking file. Also update the TotalParkings with latest number of parkings
		if i == 8:
			pt = np.array([[pts[0],pts[1]],[pts[2],pts[3]],[pts[4],pts[5]],[pts[6],pts[7]]], np.int32)
			pt = pt.reshape((-1,1,2))
    			cv2.polylines(img,[pt],True,(255,0,0))
    			#cv2.rectangle(img,(min(pts[0],pts[2]),min(pts[1],pts[3])),(min(pts[0],pts[2])+abs(pts[0]-pts[2]),min(pts[1],pts[3])+abs(pts[1]-pts[3])),(255,0,0),2)
    			cv2.imshow('image', img)
    			i=0
    			fo.close()
    			j=j+1
    			fo = open('TotalParkings.txt','w')
    			fo.write(str(j)+"\n")
    			fo.close()

#initI()
print i
parkingSpacesFull = []
cv2.imshow('image', img)
cv2.setMouseCallback('image',mousePosition)   
parkingSpaces=drawParkings(j)

for i in range(0,j):
	parkingSpacesFull.append(0)
	
cascade_src = 'cars.xml'
car_cascade = cv2.CascadeClassifier(cascade_src)

cars = car_cascade.detectMultiScale(img, 1.1, 1)

for (x,y,w,h) in cars:
       cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
       poly=Polygon(((x,y),(x+w,y),(x+w,y+h),(x,y+h)))
       for i in range(0,j):
       		if parkingSpacesFull[i] != 1: 
       			intersectArea=poly.intersection(parkingSpaces[i]).area
       			if (intersectArea>0):
       				if ((intersectArea/poly.area)>0.55 or (intersectArea/parkingSpaces[i].area)>0.55):
       					parkingSpacesFull[i]=1
for i in range(0,j):
	print 'Parking '+str(i+1)+'->'+str(parkingSpacesFull[i])
       		
cv2.imshow('image', img)
cv2.waitKey(0)
#img = cv2.GaussianBlur(img,(3,3),0)
    
cv2.waitKey(0)
fo.close()		   	
cv2.destroyAllWindows()