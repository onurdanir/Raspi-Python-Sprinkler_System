import time

#role
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import Adafruit_DHT
from time import sleep
import os

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import RPi.GPIO as GPIO
import time


#Mail
COMMASPACE = ', '

def SendEMail():
    sender = 'destek@onurdanir.com'
    gmail_password = 'fc97F.gB-LZ@@64i'
    recipients = ['destek@onurdanir.com']
    
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Çiçekler susuz kaldı ve sulama yapılıyor'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

   

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('mail.onurdanir.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise
#


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

TRIG = 14
ECHO = 15
i = 0

#relay
GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(13, GPIO.IN)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(19, GPIO.IN)
GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(26, GPIO.IN)
GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)




dist_from_base = 100  # Write the distance from the sensor to the base of the bucket
#GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
# GPIO.setup(4 ,GPIO.OUT)


# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), outline=0, fill=0)

padding = 2
shape_width = 20
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Load default font.
font = ImageFont.load_default()
font18 = ImageFont.truetype('Minecraftia.ttf', 18)
font20 = ImageFont.truetype('Minecraftia.ttf', 20)
font24 = ImageFont.truetype('Minecraftia.ttf', 24)


# Write two lines of text.
draw.text((x + 13, top), 'Loading...', font=font18, fill=255)
draw.text((x + 25, 28), 'Developer By', font=font, fill=255)
draw.text((x + 5, 38), 'Onur Danır', font=font18, fill=255)

# Display image.
disp.image(image)
disp.display()

sensor = Adafruit_DHT.DHT11
pin = 4

GPIO.output(TRIG, False)
print("Starting.....")
time.sleep(2)

while True:
    
    #relay1
    if GPIO.input(6) == 1:
        print("1.Saksıda suya ihtiyaç var")
        #sleep(1)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x + 15, top), 'Sulama', font=font24, fill=255)
        draw.text((x, 30), 'Yapılıyor', font=font24, fill=255)
        disp.image(image)
        disp.display()
        #SendEMail()
        GPIO.output(12, GPIO.LOW)
        while (True):
            if not GPIO.input(6):
                GPIO.output(12, GPIO.HIGH)
                break
    else:
        print("1.Saksıda suya ihtiyaç yok")
    
    #relay2
    if GPIO.input(13) == 1:
        print("2.Saksıda suya ihtiyaç var")
        #sleep(1)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x + 15, top), 'Sulama', font=font24, fill=255)
        draw.text((x, 30), 'Yapılıyor', font=font24, fill=255)
        disp.image(image)
        disp.display()
        #SendEMail()
        GPIO.output(16, GPIO.LOW)
        while (True):
            if not GPIO.input(13):
                GPIO.output(16, GPIO.HIGH)
                break
    else:
        print("2.Saksıda suya ihtiyaç yok")
    
    #relay3
    if GPIO.input(19) == 1:
        print("3.Saksıda suya ihtiyaç var")
        #sleep(1)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x + 15, top), 'Sulama', font=font24, fill=255)
        draw.text((x, 30), 'Yapılıyor', font=font24, fill=255)
        disp.image(image)
        disp.display()
        #SendEMail()
        GPIO.output(20, GPIO.LOW)
        while (True):
            if not GPIO.input(19):
                GPIO.output(20, GPIO.HIGH)
                break
    else:
        print("3.Saksıda suya ihtiyaç yok")
    
    
    #relay4
    if GPIO.input(26) == 1:
        print("4.Saksıda suya ihtiyaç var")
        #sleep(1)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x + 15, top), 'Sulama', font=font24, fill=255)
        draw.text((x, 30), 'Yapılıyor', font=font24, fill=255)
        disp.image(image)
        disp.display()
        #SendEMail()
        GPIO.output(21, GPIO.LOW)
        while (True):
            if not GPIO.input(26):
                GPIO.output(21, GPIO.HIGH)
                break
    else:
        print("4.Saksıda suya ihtiyaç yok")
    
    

    

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_stop = time.time()

    pulse_time = pulse_stop - pulse_start

    distance = pulse_time * 17150
    distance = round(distance)
    percentage = (distance * 100) / dist_from_base
    percentage = 100 - percentage
    percentage = round(percentage, 2)
    percentage = str(percentage)
    if distance > dist_from_base:
        distance = dist_from_base
    print(round(distance, 2));
    #draw.rectangle((0, 0, width, height), outline=0, fill=0)
    distance = str(distance)
    sleep(2)

   
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        sleep(2)
        str_temp = ' {0:0} C '.format(temperature)
        str_hum = ' {0:0} %'.format(humidity)
        print('Temp={0:0}C  Humidity={1:0}%'.format(temperature, humidity))
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        # disp.clear()
        # disp.display()
        draw.text((x, top), 'ISI:', font=font18, fill=255)
        draw.text((x + 60, top), str_temp, font=font18, fill=255)
        draw.text((x, 21), 'NEM:', font=font18, fill=255)
        draw.text((x + 60, 21), str_hum, font=font18, fill=255)
        
        
        draw.text((x, 42), 'SU:', font=font18, fill=255)
        draw.text((x + 65, 42), percentage, font=font18, fill=255)
        draw.text((x + 112, 42), '%', font=font18, fill=255)
        
        
        #disp.image(image)
        #disp.display()
    else:
        #continue
        print('Failed to get reading. Try again!')
        sleep(2)
   
   
   
   
   
   
    
    # Display image.
    disp.image(image)
    disp.display()
    distance = float(distance)
    time.sleep(2)
    #disp.clear()
    #draw.rectangle((0, 0, width, height), outline=0, fill=0)
