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
         console.log("THISOIH")

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
   temp.forEach((row) => students.push(row.split(",")));
   filterNames(students);
}

let NumberOfNames = 0;

const Colors = {
   "S": "#3da01c",
   "I": "#2b28cc",
   "P": "#651ca0",
   "A": "#1b9496",
   "V": "#c19a19",
   "C": "#ce7137"
}
const ColorsH = {
   "S": "#8bcc76",
   "I": "#9a99ff",
   "P": "#733da0",
   "A": "#579596",
   "V": "#c1af74",
   "C": "#cea890"
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

var OldNumberFlag = false
var inputID = document.getElementById("IDCard");
inputID.addEventListener("keydown", function (event) {
   if (OldNumberFlag) {
      inputID.value = ""
      inputID.style.backgroundColor = ""
      OldNumberFlag = false
   }
   // If the user presses the "Enter" key on the keyboard
   if (event.key === "Enter") {
      OldNumberFlag = true
      if (inputID.value.length == 10) {
         // Cancel the default action, if needed
         inputID.style.backgroundColor = "#8F8"
      }
      if (inputID.value.length != 10) {
         inputID.style.backgroundColor = "#F88"
      }
   }
   if (event.key === "Escape") {
      inputID.style.backgroundColor = ""
      inputID.value = ""
      OldNumberFlag = false
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

function flashEffect(element) {
   let flashCount = 0;

   function flash() {
      if (flashCount < 6) { // Flash twice (4 states: 2 off + 2 on)
         element.style.backgroundColor = flashCount % 2 === 0 ? "yellow" : "";
         flashCount++;
         setTimeout(flash, 100); // 0.75 seconds
      }
   }

   flash();
}


function select(ID) {
   if (inputID.value.length != 10) {
      flashEffect(inputID)
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
