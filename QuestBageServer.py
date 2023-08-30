from http.server import BaseHTTPRequestHandler, HTTPServer
import os 
import time
import base64

import csv

# check if needed folders and files exist before starting.
if not os.path.isdir("CSV"):
    os.mkdir("CSV")
if not os.path.exists(os.path.join(".","CSV","user-export.csv")):
    print(f"Error: file `{os.path.join('.','CSV','user-export.csv')}` dose not exist.")
    exit(1)
if not os.path.isdir("AllPDFS"):
    os.mkdir("AllPDFS")
if not os.path.isdir("AllPhotos"):
    os.mkdir("AllPhotos")


# import after checks becuse Template.py uses them
import Template


hostName = "localhost"
serverPort = 8080
#Making global variables for dynamic pdf and pixs
NewPDF=""
def setPDF(new):
   global NewPDF
   NewPDF = new
def getPDF():
   global NewPDF
   return NewPDF

NewPIX=""
def setPIX(new):
   global NewPIX
   NewPIX = new
def getPIX():
   global NewPIX
   return NewPIX

RFID=""
def setRFID(new):
   global RFID
   RFID = new
def getRFID():
   global RFID
   return RFID

def SaveRFIDName(ID,Name):
   file_exists = os.path.exists(os.path.join(".","CSV","RFID_Names.csv"))
   with open(os.path.join(".","CSV","RFID_Names.csv"), 'a', newline='') as csv_file:
      csv_writer = csv.writer(csv_file)
      if not file_exists:
         csv_writer.writerow(['RFID Number', 'Name'])
   
      csv_writer.writerow([str(ID),str(Name)])

   return

class MyServer(BaseHTTPRequestHandler):
   #All get request go through heare some how IDK
   def do_GET(self):
      print(self.path)
      #Main page also know as index This page is the only public facing one
      if self.path == ('/' or "/index.html"):
         self.send_response(200)
         self.send_header("Content-type", "text/html")
         self.end_headers()
         with open("webServer/index.html",'rb') as f:
            self.wfile.write(f.read())
      #CSS file for nice formatting.
      if self.path == ('/index.css'):
         self.send_response(200)
         self.send_header("Content-type", "text/css")
         self.end_headers()
         with open("webServer/index.css",'rb') as f:
            self.wfile.write(f.read())
      #Javascript file for custom javascript stuff Just look up what Javascript does.
      if self.path == ('/index.js'):
         self.send_response(200)
         self.send_header("Content-type", "text/javascript")
         self.end_headers()
         with open("webServer/index.js",'rb') as f:
            self.wfile.write(f.read())
      #CSV file for searching function Also same file Students.py uses
      if self.path == ('/user-export.csv'):
         self.send_response(200)
         self.send_header("Content-type", "text/csv")
         self.end_headers()
         with open(os.path.join(".","CSV","user-export.csv"),'rb') as f:
            self.wfile.write(f.read())
         Template.CSVReload()
      if self.path == ('/ThisIsFine.pdf'):
         self.send_response(200)
         self.send_header("Content-type", "application/pdf")
         self.end_headers()
         with open(os.path.join(".","Templates","ThisIsFine.pdf"),'rb') as f:
            self.wfile.write(f.read())
      #The server receives the id in format /ID?S050301 and return the name of the person 
      if self.path.split("?")[0] == ("/ID"):
         afterString = self.path.split("?")[1]
         afterStringSplit = afterString.split("&")
         #check if there are arguments in the path
         if(len(afterStringSplit)==2):
            self.send_response(200)
            self.send_header("Content-Type","text/text")
            self.end_headers()
            #Makes the badge returns the name of the pdf and the name of the pix, Takes ID string
            temp,temp2 = Template.makePDF(afterStringSplit[0].upper(),getPIX())
            #setting global variables
            setPDF(temp)
            setPIX(temp2)
            SaveRFIDName(afterStringSplit[1],temp[0:-4])

            #Returns the Name with dash instead of space
            self.wfile.write(os.path.join("",temp).encode('utf-8'))
            setRFID("")
         else:
            self.send_response(400)
            self.send_header("Content-Type","text/text")
            self.end_headers()
      #Get the last pdf that was recreated. getPDF is only updated in /ID
      if self.path == ("" if getPDF() == "" else "/"+getPDF()):
         self.send_response(200)
         self.send_header("Content-type", "application/pdf")
         self.end_headers()
         print("GETPDF")
         print(getPDF())
         print(os.path.join(".","AllPDFS",str(getPDF())))
         with open(os.path.join(".","AllPDFS",str(getPDF())),'rb') as f:
            self.wfile.write(f.read())
      
      # if self.path == "/PDF":
      #    self.send_response(200)
      #    self.send_header("Content-type", "text/csv")
      #    # self.send_header('Access-Control-Allow-Origin', '*')
      #    self.end_headers()
      #    with open(NewPDF,'rb') as f:
      #       self.wfile.write("data:image/png;base64,"+base64.standard_b64encode(f.read().encode("ascii")))

   def do_POST(self):
      #Get the picture and saves it
      if self.path == ("/Pix"):
         #http stuff and magic
         content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
         post_data = self.rfile.read(content_length) # <--- Gets the data itself
         self.send_response(200)
         self.send_header("Content-Type","image/png")
         self.end_headers()
         self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
         
         #decodes the string and removes the web compliance stuff and reencodes it for base64 lib
         justString = post_data.decode("ascii")
         justString = justString.replace("data:image/png;base64,","")
         justString = justString.encode("ascii")
         imageDecoded = base64.standard_b64decode(justString)
         #saves the image in TEMP as we dont know the name yet
         imageResult = open("TEMP.png","wb")
         #Set the global variable of PIX to TEMP
         setPIX("TEMP.png")
         imageResult.write(imageDecoded)
         imageResult.close()
      '''
      if self.path == ("/Number"):
         content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
         post_data = self.rfile.read(content_length) # <--- Gets the data itself
         self.send_response(200)
         self.send_header("Content-Type","text/number")
         self.end_headers()
         self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
         setRFID(post_data.decode("ascii"))
         print(justString)
         '''



if __name__ == "__main__":    
  webServer = HTTPServer((hostName, serverPort), MyServer)
  print("Server started http://%s:%s" % (hostName, serverPort))

  try:
    webServer.serve_forever()
  except KeyboardInterrupt:
    pass

  webServer.server_close()
  print("Server stopped.")