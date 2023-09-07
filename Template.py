import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import sys
import csv
import datetime
import requests
from io import BytesIO

#Set up stuff
fontDir = "Fonts"
TitleFont = ImageFont.truetype(os.path.join(fontDir,'NotoSansCJK-Regular.ttc'), 50)
ExtraWordsFont = ImageFont.truetype(os.path.join(fontDir,'NotoSerif-Regular.ttf'), 50)
NameFont = os.path.join(fontDir,'NotoSansCJK-Bold.ttc')
CSVName = os.path.join(".","CSV","user-export.csv")
TitleLookUp = {"I":"Instructor","A":"Admin","P":"Parent","S":"Student"}

# Students = []
# with open(CSVName,"r") as file:
#    reader = csv.reader(file)
#    for row in reader:
#       Students.append(row)

Students = {}
#reload csv file
def CSVReload():
    global Students  
    with open(CSVName,encoding='utf-8-sig', mode='r') as f:
        data = csv.reader(f)
        Students = {rows[0]:f'{rows[1].strip().title()}\n{rows[2].strip().title()}' for rows in data}

#Loads the csv file into dictionary for quick look up
CSVReload()

#automatically update the date
def getYear():
    today = datetime.date.today()
    if today.month >= 7:
        startYear = today.year
    else:
        startYear = today.year - 1
    endYear = startYear + 1
    
    return f"{startYear}-{str(endYear)[2:]}"

#counting characters in string length this can should be shortened to len(string) but it works for now/
def charInString(input_string):
   letter_count = 0
   for char in input_string:
      if char.isalpha():
         letter_count += 1
   return letter_count

#generates qrcode and puts it on the template image
def addQrCode(Code,BaseImage,QrOffset,w,h):
   qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H,box_size = 10,border=2)
   qr.add_data(Code)
   qr.make(fit=True)
   qr = qr.make_image(fill_color="black",back_color="white")
   wq,hq = qr.size
   BaseImage.paste(qr,(w-wq-QrOffset,h-hq-QrOffset))
   return BaseImage

#adds the face and border in a specific position 
def addFaceAndBorder(img,FaceName,maxsize,FacePos,FaceBorderWidth):
   Face = Image.open(FaceName)
   Face = Face.crop(((Face.size[0]-Face.size[1])/2,0,Face.size[0]-(Face.size[0]-Face.size[1])/2,Face.size[1]))
   Face.thumbnail((maxsize,maxsize), Image.LANCZOS)
   wF,hF = Face.size
   img.paste(Face,FacePos)
   draw = ImageDraw.Draw(img)
   draw.rectangle([FacePos,(FacePos[0]+wF,FacePos[1]+hF)],outline ="Black",width=FaceBorderWidth)
   return img,draw

def addURLImage(img,URL,maxsize,Pos,FaceBorderWidth):
   response = requests.get(URL,timeout=5)
   if response.status_code == 200:
      DLImage = Image.open(BytesIO(response.content))
   DLImage = DLImage.crop(((DLImage.size[0]-DLImage.size[1])/2,0,DLImage.size[0]-(DLImage.size[0]-DLImage.size[1])/2,DLImage.size[1]))
   DLImage.thumbnail((maxsize,maxsize), Image.LANCZOS)
   wF,hF = DLImage.size
   img.paste(DLImage,Pos,DLImage)
   return img

#Adds the tilde with new line for first and last name
def topWords(draw,Name,font,w,h,wOffset=0,hOffset=0,addedOffset=0):
   tempHight=0
   for PartName in Name.rsplit("\n"):
      _, _, wd, hd = draw.textbbox((0, 0), PartName, font=font)
      draw.text(((w-wd)/2-wOffset,hOffset+tempHight), PartName,font = font, fill="black",)
      tempHight=hd+tempHight+addedOffset
   return draw

#adds type of person, and year
def addSideText(draw,title,font,HightOffset,w,h,FacePos,maxsize):
   _, _, wd, hd = draw.textbbox((0, 0), title, font=font)
   draw.text((((w-(FacePos[0]+maxsize)-wd)/2)+(FacePos[0]+maxsize),FacePos[1]+HightOffset), title,font = font, fill="black")
   return hd+HightOffset

#The main program part
def MakeStudentPDF(Code, PhotoPath):
   #gets the student name if it fails return -1 and quit loop
   RawName = Students.get(Code,-1)
   if(RawName == -1):
      return 1
   Name=RawName
   #set up stuff
   title = TitleLookUp.get(Code[0],"Unknown")
   Year = getYear()
   ExtraWords = "Quest for Education\n& Arts, Inc."

   QrOffset = 50
   maxsize = 300
   FacePos = (50,350)
   nameFromTop = 75
   FaceBorderWidth=4
   template = Image.open("./Templates/"+title+"Template.png")

   Num = charInString(Name)
   #making the name have \n (New Line) instead of spaces
   tmp = Name.rsplit("$", 1)
   Name = "\n".join(tmp)

   #setting fontsize based on length of persons name
   if Num <= 14:
      font = ImageFont.truetype(NameFont, 85)
   elif Num <= 20:
      font = ImageFont.truetype(NameFont, 70)
   elif Num <= 25:
      font = ImageFont.truetype(NameFont, 70)
   
   w,h = template.size

   template = addQrCode(Code,template,QrOffset,w,h) #Qr Code
   if Code[1:] == "050301":
      template = addURLImage(template,"https://avatars.githubusercontent.com/u/44046537?v=0",110,(188,725),0) #David
   template,draw = addFaceAndBorder(template,PhotoPath,maxsize,FacePos,FaceBorderWidth) #Face
   topWords(draw,Name,font,w,h,hOffset=nameFromTop) #Name
   TitleH = addSideText(draw,title,TitleFont,75,w,h,FacePos,maxsize)#Title student, teacher, ....
   DateH = addSideText(draw,Year,TitleFont,TitleH+20,w,h,FacePos,maxsize) #Date
   topWords(draw,ExtraWords,ExtraWordsFont,w,h,FacePos[1]+maxsize+15) #Adds Quest for education and arts

   #Saving stuff
   template = template.convert('RGB')
   tmp = RawName.rsplit(" ")
   Name = "-".join(tmp)
   tmp = Name.rsplit("\n")
   Name = "-".join(tmp)
   print("Makeer "+Name)
   template.save(f"./AllPDFS/{Name}.pdf",quality=95,resolution=300)
   #if the file is run by itself then dont save the picture
   if __name__ != "__main__": 
      if os.path.isfile(f"./AllPhotos/{Name}.{PhotoPath.split('.')[-1]}") and PhotoPath == "TEMP.png":
         os.remove(f"./AllPhotos/{Name}.{PhotoPath.split('.')[-1]}")
      if PhotoPath == "TEMP.png":
         os.rename(PhotoPath,f"./AllPhotos/{Name}.{PhotoPath.split('.')[-1]}")
   #img.show()
   #Return name of pdf and picture 
   return f"{Name}.pdf" , os.path.join(".","AllPhotos",f"{Name}.{PhotoPath.split('.')[-1]}")

#The main program part
def MakeTeacherPDF(Code, PhotoPath="Face2.jpg"):
   #gets the student name if it fails return -1 and quit loop
   RawName = Students.get(Code,-1)
   if(RawName == -1):
      return 1
   Name=RawName
   #set up stuff
   title = TitleLookUp.get(Code[0],"Unknown")
   Year = "2023-24   "+title
   ExtraWords = "Quest for\nEducation\n& Arts, Inc."

   QrOffset = 50
   maxsize = 300
   FacePos = (50,50)
   nameFromTop = 50
   FaceBorderWidth=4
   nameLeftOffset=-175
   template = Image.open("./Templates/"+title+"Template.png")

   Num = charInString(Name)
   #making the name have \n (New Line) instead of spaces
   # tmp = Name.rsplit(" ", 1)
   # Name = "\n".join(tmp)

   #setting fontsize based on length of persons name
   if Num <= 14:
      font = ImageFont.truetype(NameFont, 80)
   elif Num <= 20:
      font = ImageFont.truetype(NameFont, 70)
   else:
      font = ImageFont.truetype(NameFont, 70)
   
   w,h = template.size

   template = addQrCode(Code,template,QrOffset,w,h) #Qr Code
   template,draw = addFaceAndBorder(template,PhotoPath,maxsize,FacePos,FaceBorderWidth) #Face
   topWords(draw,Name,font,w,h,nameLeftOffset,hOffset=nameFromTop,addedOffset=-16) #Name
   addSideText(draw,Year,TitleFont,200,w,h,FacePos,maxsize)#Date + Title student, teacher, ....
   topWords(draw,ExtraWords,ExtraWordsFont,w,h,hOffset=FacePos[1]+maxsize+15,addedOffset=10) #Adds Quest for education and arts

   #Saving stuff
   template = template.convert('RGB')
   tmp = RawName.rsplit(" ")
   Name = "-".join(tmp)
   tmp = Name.rsplit("\n")
   Name = "-".join(tmp)
   print("Makeer "+Name)
   template.save(f"./AllPDFS/{Name}.pdf",quality=90,resolution=300)
   #if the file is run by itself then dont save the picture
   if __name__ != "__main__":
      if os.path.isfile(f"./AllPhotos/{Name}.{PhotoPath.split('.')[-1]}") and PhotoPath == "TEMP.png":
         os.remove(f"./AllPhotos/{Name}.{PhotoPath.split('.')[-1]}")
      if PhotoPath == "TEMP.png":
         os.rename(PhotoPath,f"./AllPhotos/{Name}.{PhotoPath.split('.')[-1]}")
   #img.show()
   #Return name of pdf and picture 
   return f"{Name}.pdf" , os.path.join(".","AllPhotos",f"{Name}.{PhotoPath.split('.')[-1]}")

#make guest
def makeNumbers(Name):
   guestPDF = os.path.join("Templates",f"{Name}.png")
   numFile = os.path.join("CSV",f"{Name}.number")
   guestNumber = 1
   if not os.path.isfile(numFile):
      with open(numFile,'w') as f:
         f.write(str(guestNumber))
   else:
      with open(numFile,'r') as f:
         guestNumber = 1+int(f.readline())
   template = Image.open(guestPDF)
   w,h = template.size
   draw = ImageDraw.Draw(template)
   addSideText(draw,f"{guestNumber:04d}",TitleFont,0,w,h,(-750,925),300)
   print(guestNumber)
   with open(numFile,'w') as f:
         f.write(str(guestNumber))
   template = template.convert('RGB')
   template.save(os.path.join(".","AllPDFS",f"{Name}-{guestNumber:04d}.pdf"),quality=95,resolution=300)
   return f"{Name}-{guestNumber:04d}.pdf", os.path.join(".","AllPDFS",f"{Name}-{guestNumber:04d}.pdf")


def makePDF(Code,PhotoPath="Face2.jpg"):
   if Code[0] == "V":
      return makeNumbers("Visitor-Badge")
   if Code[0] == "C":
      return makeNumbers("Contractor-Badge")
   if Code[0] == "S":
      print("Student")
      t1,t2 = MakeStudentPDF(Code, PhotoPath)
      print(t1,t2)
      return t1,t2
   if Code[0]:
      print("Teacher")
      t1,t2 = MakeStudentPDF(Code, PhotoPath)
      print(t1,t2)
      return t1,t2

