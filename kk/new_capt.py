import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime


known_face_encoding = []

known_face_names = []

known_reg_nos = []

for imgname in os.listdir("photos"):
    img = face_recognition.load_image_file("photos/"+imgname)
    known_face_encoding.append(face_recognition.face_encodings(img)[0])
    ind = 0

    print("image name =",imgname)
    for x in range(len(imgname)-1,-1,-1):
        print("x =",x)
        # if imgname[x]=='_':
        #     ind = x
        #     break

    known_face_names.append(imgname[:ind])
    known_reg_nos.append(imgname[ind+1:])

students = known_face_names.copy()

face_locations = []
face_encoding = []
face_names = []
s = True



def DoMyWork(nm):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    name = -1
    current_time = -1
    
    
    f = open(nm+".csv","w+",newline='')
    lnwriter = csv.writer(f)
    done = False
    for x in range(30):
        if done:
            break

        _,frame = video_capture.read()
        frame = face_recognition.load_image_file("")
        if(type(frame) == type(None)):
            print("no image")
            continue;

        small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        rgb_small_frame = small_frame[:,:,::-1]
        
        done = False

        if s:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
                if name in known_face_names:
                    if name in students:
                        students.remove(name)
                        print(students)
                        current_time = now.strftime("%H-%M-%S")
                        lnwriter.writerow([name,current_time])
                    break
                else:
                    name = -1
                    current_time = -1
        print("showing frame")
        # cv2.imshow("Pl",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    # cv2.destroyWindow("pl")
    # os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
    f.close()
    if bbb==0:
        bbb = -1
    else:
        bbb = 0
    return name,current_time
