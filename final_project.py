import os,requests,smtplib,shutil, psutil,socket
from PIL import Image
from reportlab.pdfgen import canvas
from datetime import date
from email.message import EmailMessage


def img_edit():

    path = "/home/student/supplier-data/images"
    count=0

    for filename in os.listdir(path):
        if filename.lower().endswith(".tiff"): 
            img_path = os.path.join(path, filename)
            
            with Image.open(img_path) as img:  
                img = img.convert("RGB")        
                img_resized = img.resize((600, 400))  
                new_filename = f"{count:03}.jpeg"  
                new_path = os.path.join("/home/student/supplier-data/image", new_filename)
                img_resized.save(new_path, format="JPEG")
                count += 1


def img_post_to_website():

    url="http://[external-IP-address]/media/images"
    path="/home/student/supplier-data/image"

    for x in os.listdir(path):

        with open(os.path.join(path, x), 'rb') as opened:
            r = requests.post(url, files={'file': opened})
            print("Status:", r.status_code)
            print("Response:", r.text)


def txt_post_to_website():

    path ="/home/student/supplier-data/descriptions"
    url="http://[external-IP-address]/fruits"
    count=0

    for x in os.listdir(path):
        with open(os.path.join(path,x)) as txt:
            lines=txt.readlines()
            w=lines[1].split(" ")
            fruit={
                "name":lines[0],
                "weight":int(w[0]),
                "description": " ".join([line.strip() for line in lines[3:] if line.strip()]),
                "image_name":f"{count:03}.jpeg"
            }
        count+=1

        r = requests.post(url,json=fruit)
        print("Status:", r.status_code)
        print("Response:", r.text)


def createPDF():

    path ="/home/student/supplier-data/descriptions"

    c = canvas.Canvas("/tmp/processed.pdf")
    c.setFont("Helvetica", 12)
    y = 800
    c.drawString(100, y, "Processed Update on " + str(date.today()))
    y -= 40

    for x in os.listdir(path):
        
        with open(os.path.join(path,x)) as txt:
            lines=txt.readlines()
            c.drawString(100, y, "name: " + lines[0].strip())
            y -= 20
            c.drawString(100, y, "weight: " + lines[1].strip())
            y -= 20
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 800
            
    c.save()


def Generte_and_send_EMAIL():

    msg=EmailMessage()
    msg['From']='automation@example.com'
    msg['To']='student@example.com'
    msg['Subject']='Upload Completed - Online Fruit Store'
    msg.set_content('All fruits are uploaded to our website successfully. A detailed list is attached to this email.')
    with open('/tmp/processed.pdf','rb') as pdff:
        data=pdff.read()
        msg.add_attachment(
            data,
            maintype='application',
            subtype='pdf',
            filename='processed.pdf'
        )

    server2=smtplib.SMTP('127.0.0.1',25)

    server2.send_message(msg)
    server2.quit()


def check_health():
    msg = EmailMessage()
    msg['From']='automation@example.com'
    msg['To']='student@example.com'

    server2=smtplib.SMTP('127.0.0.1',25)
    total,used,free=shutil.disk_usage('/')
    mem = psutil.virtual_memory()
    mem.total      # total RAM in bytes
    mem.available  # available RAM in bytes
    mem.percent 

    if (free<(0.2*total)):
        msg['Subject']='disk'
        msg.set_content('disk space is lower than 20%')
        server2.send_message(msg)
        server2.quit()
    elif(mem.available<(100 * 1024 * 1024)):
        msg['Subject']='memory'
        msg.set_content('available memory is less than 100MB')
        server2.send_message(msg)
        server2.quit()        
    elif(psutil.cpu_percent(interval=1)>80):
        msg['Subject']='CPU'
        msg.set_content('Report an error if CPU usage is over 80%')
        server2.send_message(msg)
        server2.quit() 
    elif(socket.gethostbyname("localhost")!="127.0.0.1"):
        msg['Subject']='DNS'
        msg.set_content('the hostname localhost cannot be resolved to 127.0.0.1')
        server2.send_message(msg)
        server2.quit()       
      



def main():
    img_edit()
    img_post_to_website()
    txt_post_to_website()
    createPDF()
    Generte_and_send_EMAIL()
    check_health()

if __name__=="__main__":
    main()
