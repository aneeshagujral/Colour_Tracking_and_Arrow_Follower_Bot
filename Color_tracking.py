import cv2
import numpy as np

cap=cv2.VideoCapture(0)
up=0;
left=0;
down=0;
right=0;
    
while True:
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40,50,50])
    upper_green= np.array([80,255,255])
    
    mask= cv2.inRange(hsv, lower_green, upper_green)
    mask=cv2.erode(mask, None , iterations=2)
    mask=cv2.dilate(mask, None, iterations=2)
    #To find contours
    contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
    cnt= contours[0]
    M=cv2.moments(mask,True)
    area=cv2.contourArea(cnt)
    print " Area is ",area

    
    if(area > 10000 and area < 30000 ):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print " Centroid is", cx,cy  
        #To draw contour
        cv2.drawContours(img, contours, -1, (0,255,0), 3)
        #To draw centroid in white
        cv2.circle(img,(cx,cy),8, (255,255,255),-1)
        #To obtain minimum enclosing  circle
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(img,center,radius, (255,0,0),2)
        #To plot centre of circle on image
        cv2.circle(img,center,8, (0,0,255),-1)
        print " Center is", x,y 

        count=0;
        count1=0;
        count2=0;
        count3=0;
       
    
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            #print f
            #print s
            #print e
            #print d
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            (x1,y1)= tuple(cnt[f][0])
            print x1,y1
            print "far",far
            cv2.line(img,start,end,[0,255,0],2)
            cv2.circle(img,far,5,[0,0,255],-1)
            if cx<x1:
        #right
                count=count+1
            if cx>x1:
        #left
                count1=count1+1
            if cy<y1:
        #Down
                count2=count2+1
            if cy>y1:
        #Left
                 count3=count3+1   
            
        print "count=",count
        print "count1=",count1
        print "count2=",count2
        print "count3=",count3

        if (count>=5)and(count>count1)and(count>count2)and(count>count3):
            #print 'Right'
            right=right+1;
            #print "right",right
            if right>3:
                print 'roll no. 1'
                break
        elif (count1>=5) and (count1>count) and (count1>count2) and (count1>count3):
            #print 'Left'
            left=left+1;
            #print "left",left
            if left>3:
                print 'roll no. 2'
                break
        elif (count2>=5) and (count2>=count) and (count2>count1) and (count2>count3):
            #print 'Reverse'

            #print "down",down
            down=down+1;
            if down>3:
                print 'roll no. 3'
                break
            
        elif (count3>=5) and (count3>count) and (count3>count1) and (count3>count2):
            #print 'Straight'
            up=up+1;
            #print "up",up
            if up>3:
                print 'roll no.4'
                break
   
    
                              
        
        cv2.imshow('img',img)
        #cv2.imshow('mask' ,mask)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 
