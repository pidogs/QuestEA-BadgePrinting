var width = 1920; // We will scale the photo width to this
var height = 0; // This will be computed based on the input stream

var streaming = false;

var video = null;
var canvas = null;
var photo = null;
var startbutton = null;

function startup() {
   video = document.getElementById('video');
   canvas = document.getElementById('canvas');
   photo = document.getElementById('photo');
   startbutton = document.getElementById('startbutton');

   navigator.mediaDevices.getUserMedia({
         audio: false,
         video: {
            width: {
               min: 480,
               ideal: 1920
            },
            height: {
               min: 360,
               ideal: 1080
            }
         }

      })
      .then(function (stream) {
         video.srcObject = stream;
         video.play();
      })
      .catch(function (err) {
         console.log("An error occurred: " + err);
      });

   video.addEventListener('canplay', function (ev) {
      if (!streaming) {
         height = video.videoHeight / (video.videoWidth / width);

         if (isNaN(height)) {
            height = width;
         }

         video.setAttribute('width', width);
         video.setAttribute('height', height);
         canvas.setAttribute('width', width);
         canvas.setAttribute('height', height);
         streaming = true;
      }
   }, false);

   startbutton.addEventListener('click', function (ev) {
      takepicture();
      ev.preventDefault();
   }, false);

   clearphoto();
}


function clearphoto() {
   var context = canvas.getContext('2d');
   context.fillStyle = "#AAA";
   context.fillRect(0, 0, canvas.width, canvas.height);

   var data = canvas.toDataURL('image/png');
   photo.setAttribute('src', data);
}

let xhr = new XMLHttpRequest();

function takepicture() {
   var data;
   var context = canvas.getContext('2d');
   if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);


      data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
   } else {
      clearphoto();
   }
   xhr.open("POST", "/Pix");
   xhr.setRequestHeader("Accept", "image/png");
   xhr.setRequestHeader("Content-Type", "image/png");

   xhr.onreadystatechange = function () {
      if (xhr.readState === 4) {
         console.log(xhr.readState);
         console.log(xhr.responseText);
      }
      if (xhr.status == 200) {
         vid = document.getElementById("startbutton")
      }
   }
   xhr.send(data);

}

window.addEventListener('load', startup, false);

function printDocument() {
   //document.getElementById("print").click()
   var doc = document.getElementById("pdfDocument");
   doc.contentWindow.focus();
   doc.contentWindow.print();
   inputID.value = "";
   var input = document.getElementById("nameFilter");
   input.value = "";
   input.disabled = true;
   inputID.style.backgroundColor = "";
   filterNames();
}

function whenPrintIsReady() {
   document.getElementById("print").style.backgroundColor = "#4E4";
}


function httpGetAsync(theUrl, callback) {
   xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200)
         callback(xhr.responseText);
   }
   xhr.open("GET", theUrl, true); // true for asynchronous 
   xhr.send(null);
}

students = []

function loadNames(list) {
   temp = list.split("\r\n");
   students = []
   temp.pop()
   temp.forEach((row) => {
      rowData = row.split(",");
      properCaseName1 = rowData[1].trim().split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
      properCaseName2 = rowData[2].trim().split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
      students.push([rowData[0], properCaseName1, properCaseName2]);
   });
   filterNames(students);
}

let NumberOfNames = 0;

const Colors = {
   "S": "#3da01c",
   "I": "#2b28cc",
   "P": "#651ca0",
   "A": "#1b9496",
   "V": "#c19a19",
   "C": "#ce7137",
   "G": "#cf3849"
}
const ColorsH = {
   "S": "#8bcc76",
   "I": "#9a99ff",
   "P": "#733da0",
   "A": "#579596",
   "V": "#c1af74",
   "C": "#cea890",
   "G": "#ce7b85"
}

function makeNameElement(ID, Name) {
   let elm = document.createElement("div")
   elm.setAttribute("class", "name");
   elm.setAttribute("id", "nameSelection");
   a = "select('" + ID + "')";
   elm.setAttribute("onclick", a)
   elm.setAttribute("name", ID)
   elm.innerHTML = Name
   elm.style.backgroundColor = Colors[Array.from(ID)[0]]

   return elm
}



function filterNames() {
   var input = document.getElementById("nameFilter");
   var names = document.getElementById("names");
   let str = "";
   if (input.value == "") {
      names.innerHTML = ""
      students.forEach((row) => names.append(makeNameElement(row[0], row[1] + " " + row[2])));
   } else {
      let val = input.value.toLowerCase();
      names.innerHTML = ""
      NumberOfNames = 0;
      students.forEach(function (row) {
         OldID = ""
         let n = row[1] + " " + row[2];
         if (n.toLowerCase().includes(val)) {
            NumberOfNames++;
            names.append(makeNameElement(row[0], n))
         }
      })
      if (NumberOfNames == 0) {
         var mknameButtonName = ["Admin", "Instructor", "Parent", "Student"]
         for (let i = 0; i < mknameButtonName.length; i++) {
            var div = document.createElement("div");
            div.textContent = mknameButtonName[i];
            div.style.backgroundColor = Colors[mknameButtonName[i][0]];
            div.className = "name";
            // Add a click event listener to each div
            div.addEventListener("click", function () {
               // Get the first letter of the role name
               var firstLetter = mknameButtonName[i].charAt(0);
               var QEID = document.getElementById("QEID");
               // Get the data from the input field
               var inputData = val;
               if (QEID.value.length == parseInt(QEID.getAttribute("length"))) {
                  // Make the GET request
                  var xhr2 = new XMLHttpRequest();
                  xhr2.open("GET", `/AddName?ID=${firstLetter}${QEID.value}&Name=${inputData}`);
                  xhr2.onload = function () {
                     // console.log(xhr.readyState,xhr2.status)
                     if (xhr.readyState === 4) {
                        if (xhr2.status == 250) {
                           document.getElementById("error").style.display = "inline-block";
                           document.getElementById("nextID").innerHTML = xhr2.responseText.substring(1);
                           flashEffect(QEID, "#ff0000");
                        } else if (xhr2.status == 200) {
                           document.getElementById("error").style.display = "none";
                           httpGetAsync('/user-export.csv', loadNames);
                           filterNames();
                           setTimeout(function () {
                              document.getElementById("nameSelection").click();
                           }, 200);
                        } else {

                        }
                     }
                  }
                  xhr2.send()
               } else {
                  flashEffect(QEID, "#ffff00");
               }
            });
            names.appendChild(div);
         }

      }
   }
}

var inputName = document.getElementById("nameFilter");
inputName.addEventListener("keydown", function (event) {
   // If the user presses the "Enter" key on the keyboard
   if (event.key === "Enter" && NumberOfNames == 1) {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      document.getElementById("nameSelection").click();
   }
   if (event.key === "Escape") {
      inputName.value = ""
   }
});

var inputID = document.getElementById("IDCard");
inputID.addEventListener("input", function (event) {
   var inputName = document.getElementById("nameFilter");
   if (inputID.value.length == parseInt(inputID.getAttribute("length")) && /^\d*$/.test(inputID.value)) {
      // Cancel the default action, if needed
      inputID.style.backgroundColor = "#8F8";
      inputName.disabled = false;
   } else if (inputID.value.length != parseInt(inputID.getAttribute("length"))) {
      inputID.style.backgroundColor = "#F88"
      inputName.disabled = true;
   }
   if (event.key === "Escape") {
      inputID.style.backgroundColor = ""
      inputID.value = ""
   }
});


var QEID = document.getElementById("QEID");
QEID.addEventListener("input", function (event) {
   if (QEID.value.length == parseInt(QEID.getAttribute("length")) && /^\d*$/.test(QEID.value)) {
      // Cancel the default action, if needed
      QEID.style.backgroundColor = "#8F8";
   } else if (QEID.value.length != parseInt(QEID.getAttribute("length"))) {
      QEID.style.backgroundColor = "#F88"
   }
   if (event.key === "Escape") {
      QEID.style.backgroundColor = ""
      QEID.value = ""
   }
});


var OldID = ""

function httpGetAsync(theUrl, callback) {
   xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200)
         callback(xhr.responseText);
   }
   xhr.open("GET", theUrl, true); // true for asynchronous 
   xhr.send(null);
}

function flashEffect(element, color) {
   let flashCount = 0;

   function flash() {
      if (flashCount < 6) { // Flash twice (4 states: 2 off + 2 on)
         element.style.backgroundColor = flashCount % 2 === 0 ? color : "";
         flashCount++;
         setTimeout(flash, 150); // 0.75 seconds
      }
   }

   flash();
}


function select(ID) {
   if (inputID.value.length != 10) {
      flashEffect(inputID, "#ffff00")
      return
   }
   xhr.open("GET", "/ID?" + ID + "&" + inputID.value);
   xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200) {
         if (OldID != "") {
            document.getElementsByName(OldID)[0].style.backgroundColor = Colors[Array.from(OldID)[0]];
         }
         document.getElementsByName(ID)[0].style.backgroundColor = ColorsH[Array.from(ID)[0]];
         OldID = ID
         var doc = document.getElementById('pdfDocument');
         doc.src = xhr.responseText;
      }
   }
   xhr.send(null);
}

function valNumber(event) {
   const inputValue = event.target.value; // Access input value using 'this'
   const charCode = (event.which) ? event.which : event.keyCode;
   const char = String.fromCharCode(charCode);
   const regex = /[0-9]|\./; // Allow numbers and decimal points

   if (!regex.test(char)) {
      event.preventDefault();
      return false;
   }

   // Additional validation logic can be added here
   // For example, check decimal point placement or limit input length

   return true;
}