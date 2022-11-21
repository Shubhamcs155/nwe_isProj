let shub = false;
let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");
let click_button = document.querySelector("#click-photo");
let stop_button = document.querySelector("#stop-camera");
let canvas = document.querySelector("#canvas");
let stream;

let stp = true;
let camera_on = true;
let image_data_url;
let trial = document.getElementById("trial");
let ok = 0;

let obbj = document.getElementById("obbj");

const DEF_DELAY = 1000;

let start_capture = document.getElementById("start_capture");
let tot = 50;
let msg = -1;
let idn_name="-1";
let idn_reg ="-1";
let idn_time = "-1";

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms || DEF_DELAY));
}


camera_button.addEventListener('click', async function () {
    if (stp) {
        video.style.display = 'block';
        stream = null;
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            click_button.style.display = "block";
        }
        catch (error) {
            alert(error.message);
            return;
        }

        video.srcObject = stream;

        await sleep(300);
        click_button.style.display = 'block';
    } else {
        stream.getTracks().forEach(function (track) {
            if (track.readyState == 'live' && track.kind === 'video') {
                track.stop();
            }
        });
        video.srcObject = 'none';
        // video.style.display = 'none';
    }

});

click_button.addEventListener('click', function () {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    image_data_url = canvas.toDataURL('image/jpeg');
});

stop_button.addEventListener('click', function () {
    stp = false;
    camera_button.click();
    stp = true;
    camera_on = false;
    click_button.style.display = 'none';
    camera_button.style.display = 'inline';
});

function sndajax() {
    if(idn_name!=="-1")
        return;
    let server_data = [{ "name": image_data_url }];
    $.ajax({
        type: "POST",
        url: "/checkme",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            ok++;
            console.log(ok);
            console.log(result);

            if(result.message!==(-1)){
                idn_name = result.message.toString();
                if(idn_reg==="-1")
                    idn_reg = result.reg_no.toString();
                if(idn_time==="-1")
                idn_time = result.ctime.toString();
            }    
        }
    });
}

function addAttendence(obj){
    $.ajax({
        type: "POST",
        url: "/addnametofile",
        data: JSON.stringify(obj),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log(result);
        }
    });
}

start_capture.addEventListener('click', async function automate() {
    ok = 0;
    idn_name = "-1";
    idn_reg = "-1";
    idn_time = "-1";
    for (let i = 0; i < tot; i++) {
        if(idn_name!==("-1")){

            let correct = window.prompt(`Found name ${idn_name} and reg no ${idn_reg}`,"correct");
            if(correct!=null){
                let fname = document.getElementById("myname").value.toString();
                console.log("====================");
                console.log(fname)
                console.log("====================");
                
                if(fname===""){
                    window.alert("File name cannot be empty.Attendence not recorded.");
                    return;
                }else{
                    window.alert("you clicked right");
                    addAttendence({stud_reg:idn_reg,stud_name:idn_name,ctime:idn_time,fname:fname});
                }
                
            }else{
                window.alert("you clicked false");
            }
            break;
        }
        click_button.click();
        await sleep(100);
        try {
            await sndajax();
        } catch (error) {
            obbj.innerHTML = error;
        }
        await sleep(50);
    }
    ok = 0;
    console.clear();
});

function sendform(){
    let name = document.getElementById("studname").value;
    let reg_no = document.getElementById("studreg").value;
    let fname = document.getElementById("myname").value;
    if(name==="" || reg_no==="" || fname===""){
        alert("please fill all fields in form");
        return;
    }
    $.ajax({
        type: "POST",
        url: "/addform",
        data: JSON.stringify({stud_name:name,fname:fname,stud_reg:reg_no,}),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log(result);
            alert("Attendence added successfully");
        }
    });
}