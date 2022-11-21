from flask import Flask,render_template,request,url_for,jsonify,send_file,Response
import cv2
import numpy as np
import base64
import io
from capturer import *

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/captureAt")
def capt():
    return render_template("captureAt.html")


@app.route("/captme",methods=["GET","POST"])
def act():
    return render_template("captureAt.html")


@app.route("/checkme",methods=["GET","POST"])
def chme():
    
    if request.method=="POST":
        print("This is post request")

        bb = request.get_json()
        data_url = bb[0]["name"]
        
        data_url = data_url[23:] ;
        string = data_url
        
        string = bytes(string, encoding="raw_unicode_escape")
        jpg_original = base64.b64decode(string)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        cv2.imwrite('./Test/0.jpg', img)
        msg,reg_no,ctime = DoMyWork()
        
        result = {"message":msg,"reg_no":str(reg_no),"ctime":ctime}
        return jsonify(result)

@app.route("/addnametofile",methods=["POST"])
def addName():
    revert();
    data = request.get_json()
    print("got data")
    print("<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>")
    print(data)
    print(type(data))
    print("<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>")
    # stud_reg = data["stud_reg"]
    # stud_name = data["stud_name"]
    # ctime = data["ctime"]
    # fname = data["fname"]
    # stud_reg = data[0]["stud_reg"]
    print("===================")
    # print(stud_reg)
    stud_name = "temp"
    try:
        stud_name = data["stud_name"]
    except Exception as e:
        print(e);
    ctime = data["ctime"]
    fname = data["fname"]
    stud_reg = data["stud_reg"]
    addNameToFile(stud_reg,stud_name,ctime,fname)
    result = {"message":stud_name+" "+stud_reg + "Recorded successfully !"}
    return jsonify(result)

@app.route("/addnewphoto",methods=["POST"])
def addNewPhoto():
    if request.method=="POST":
        data = request.get_json()
        data_url = data[0]["photo"]
        name = data[0]["name"]
        reg_no = data[0]["reg_no"]

        data_url = data_url[23:]
        data_url = bytes(data_url,encoding="raw_unicode_escape")
        jpg_original = base64.b64decode(data_url)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        cv2.imwrite("./photos/"+name+"_"+reg_no+".jpg", img)
        result = {"message":"Photo added successfully"}
        return jsonify(result)

@app.route("/allFiles",methods=["GET"])
def listFiles():
    csvs = []
    for imgname in os.listdir():
        if(imgname[len(imgname)-3:]=="csv"):
            csvs.append(imgname)
    csvs.sort()
    ids = []
    for fl in csvs:
        ids.append(fl[:len(fl)-4])
    return render_template("allSheets.html",flLst=csvs,lsLen=len(csvs),lsId=ids)

@app.route("/sendfile",methods=["GET"])
def sendFile():
    try:
        fname = request.args.get("fname")
        return send_file(fname+".csv",mimetype='text/csv',download_name=fname+".csv",as_attachment=True)

    except Exception as e:
        print("failed to send file")
        return str(e)

@app.route("/addform",methods=["POSt"])
def addNameF():
    data = request.get_json()

    stud_name = data["stud_name"]
    now = datetime.now()
    ctime = str(now.strftime("%H-%M-%S"))
    fname = data["fname"]
    stud_reg = data["stud_reg"]
    f = open(fname+".csv","w+",'a')
    lnwriter = csv.writer(f)
    lnwriter.writerow([stud_reg,stud_name,ctime])
    f.close()
    print("name "+stud_name+" added to file "+fname+" successfully");
    result = {"message":stud_name+" "+stud_reg + "Recorded successfully !"}
    return jsonify(result)

if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True,port=5200)