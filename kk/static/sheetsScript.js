function downLoadFile(nm){
    let sndData = {"fname":nm}
    window.alert(nm)
    // window.alert("hello world")
    document.location.href = "http://127.0.0.1:5200/sendfile?fname="+nm;
    // document.location.href = "http://127.0.0.1:5200/allFiles";
    // $.ajax({
    //     type: "GET",
    //     url: "/sendfile",
    //     data: JSON.stringify(sndData),
    //     contentType: "application/json",
    //     xhrFields: {
    //         responseType: 'blob'
    //     },
    //     dataType: 'json',
    //     success: function (result) {
    //         // msg = result.message;
    //         console.log("got response")
    //         console.log(result)
    //         // window.alert("File downloaded successfully")
    //     }
    // });
}
// function downLoadFile(nm){
//     let sndData = {"fname":nm}
//     window.alert(nm)
//     // window.alert("hello world")
//     $.ajax({
//         type: "GET",
//         url: "/sendfile",
//         data: JSON.stringify(sndData),
//         contentType: "application/json",
//         xhrFields: {
//             responseType: 'blob'
//         },
//         dataType: 'json',
//         success: function (result) {
//             // msg = result.message;
//             console.log("got response")
//             console.log(result)
//             // window.alert("File downloaded successfully")
//         }
//     });
// }