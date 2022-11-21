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

    for x in range(len(imgname)-1,-1,-1):
        if imgname[x]=='_':
            ind = x
            break

    known_face_names.append(imgname[:ind])
    known_reg_nos.append(imgname[ind+1:])

students = known_face_names.copy()

face_locations = []
face_encoding = []
face_names = []
done = False
# s = True

tot_itr = 1
test_reg_no = -1
last_removed_name = "-1"

def DoMyWork():
    now = datetime.now()
    test_reg_no = -1
    current_date = now.strftime("%Y-%m-%d")
    name = -1
    current_time = "-1"
    
    done = False
    for x in range(tot_itr):
        if done:
            break
        print("checking")
        frame = face_recognition.load_image_file("Test/0.jpg")
        if(type(frame) == type(None)):
            print("no image")
            continue;

        small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        rgb_small_frame = small_frame[:,:,::-1]
        
        done = False

        
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
            if name in known_face_names and name in students:
                test_reg_no = known_reg_nos[known_face_names.index(name)]
                students.remove(name)
                last_removed_name = name
                print(students)
                current_time = now.strftime("%H-%M-%S")
                done = True
                break
            else:
                name = -1


    print("==========================")
    print("Done =",done);
    return name,test_reg_no,current_time

def addNameToFile(reg_no,name,ctime,fname):
    f = open(fname+".csv","w+",'a')
    lnwriter = csv.writer(f)
    lnwriter.writerow([reg_no,name,ctime])
    f.close()
    print("name "+name+" added to file "+fname+" successfully");

def revert():
    global last_removed_name
    global done
    if last_removed_name!="-1" and done:
        if last_removed_name not in students:
            students.append(last_removed_name)
        last_removed_name = "-1"