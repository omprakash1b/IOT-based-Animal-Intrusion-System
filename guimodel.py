from tkinter import *
import tkinter as tk
import cv2
import urllib.request
import numpy as np
import pickle
import os
from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = ""  # Replace with your Twilio Account SID
AUTH_TOKEN = ""    # Replace with your Twilio Auth Token
TWILIO_PHONE_NUMBER = ""  # Replace with your Twilio number

# Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

root = tk.Tk()
root.geometry('450x150') 

url = ''

Label(root, text='Cam server').pack()
e1 = Entry(root)
e1.pack()


def otp(s):
    try:
                
        message = client.messages.create(
                    body=f"Animal Intrusion detected {s}",
                    from_=TWILIO_PHONE_NUMBER,
                    to=""
        )
        print({'message': 'OTP sent successfully', 'sid': message.sid})
    except Exception as e:
        print({'error': str(e)})


def fun():
    
    cv2.namedWindow("Live Cam Testing", cv2.WINDOW_AUTOSIZE)
    model_path = r'C:\\Users\\Om Prakash\\OneDrive\\Desktop\\final project\\model.pkl'
    url = e1.get()
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        exit()

    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
            print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        exit()

    while True:
        try:
            
            img_resp = urllib.request.urlopen(url)
            img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

            
            if frame is None:
                print("Failed to fetch or decode the frame. Skipping...")
                continue

            
            try:
                results = model.predict(source=frame, show=True, conf=0.5)
                print(f"Detections: {results}")
                object_counts = {}
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        class_id = box.cls.item()
                        class_name = model.names[class_id]
                        object_counts[class_name] = object_counts.get(class_name, 0) + 1
            
                s=''
                se = False
                listl = ['cat', 'dog', 'horse','sheep','cow', 'elephant','bear', 'zebra', 'giraffe', 'bird',]
                for class_name, count in object_counts.items():
                    s+=f"{class_name}: {count}"+"\n"
                    if class_name in listl:
                        se = True

                if se :
                    otp(s)

            except Exception as e:
                print(f"Error during object detection: {e}")
                continue

            
            cv2.imshow('Live Cam Testing', frame)

        except Exception as e:
            print(f"Error fetching or processing frame: {e}")
            break

        
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


button = tk.Button(root, text="Click Me", activebackground="blue", activeforeground="white",command=fun)
button.pack()


root.mainloop()


