import cv2
import face_recognition
from twilio.rest import Client
import datetime
from geopy.geocoders import Nominatim
import numpy as np
import sounddevice as sd

account_sid = 'Your id'
auth_token = 'token'
twilio_phone_number = 'twilio num'
owner_phone_number = 'owner number'
police_phone_number = '+1234567890' 

owner_images = [
    face_recognition.load_image_file('C:/Users/91979/Documents/sample.jpg')
]
owner_encodings = [face_recognition.face_encodings(image)[0] for image in owner_images]

ip_webcam_url = 'http://192.168.200.41:4747/video'

video_capture_phone = cv2.VideoCapture(ip_webcam_url)

video_capture_laptop = cv2.VideoCapture(0)


last_alert_time = None

unrecognized_person_count = 0

prev_unrecognized_person = None


geolocator = Nominatim(user_agent='camera_location')
location = geolocator.geocode('')
if location is not None:
    camera_location = location.address
else:
    camera_location = 'India'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = None
is_video_saving = False

fs = 44100  
duration = 1 
silence_threshold = 0.01  

while True:
   
    ret_phone, frame_phone = video_capture_phone.read()
    ret_laptop, frame_laptop = video_capture_laptop.read()

    frame_phone = cv2.resize(frame_phone, (int(frame_phone.shape[1] / 2), int(frame_phone.shape[0] / 2)))
    frame_laptop = cv2.resize(frame_laptop, (int(frame_phone.shape[1]), int(frame_phone.shape[0])))

    rgb_frame_phone = frame_phone[:, :, ::-1]


    face_locations = face_recognition.face_locations(rgb_frame_phone)
    face_encodings = face_recognition.face_encodings(frame_phone, face_locations)


    unrecognized_person_detected = False
    armed_person_detected = False

    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(owner_encodings, face_encoding)
        if not any(matches):

            unrecognized_person_detected = True

       
            if prev_unrecognized_person is not None:
                if face_recognition.compare_faces([prev_unrecognized_person], face_encoding)[0]:
              
                    continue

            unrecognized_person_count += 1

            cv2.imwrite(f'unrecognized_person_{unrecognized_person_count}.jpg', frame_phone)

            prev_unrecognized_person = face_encoding

            break

    if unrecognized_person_detected:
        if last_alert_time is None or (datetime.datetime.now() - last_alert_time).seconds >= 10:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            client = Client(account_sid, auth_token)

            body = 'Unrecognized person detected at {}. Count: {}. Location: {}'.format(
                current_time, unrecognized_person_count, camera_location)

            message = client.messages.create(
                body=body,
                from_=twilio_phone_number,
                to=owner_phone_number
            )
            print('Alert sent to owner!')

            last_alert_time = datetime.datetime.now()

    if output_video is not None:
        output_video.write(cv2.hconcat([frame_phone, frame_laptop]))

    combined_frame = cv2.hconcat([frame_phone, frame_laptop])
    cv2.imshow('Video', combined_frame)

    gray_frame_laptop = cv2.cvtColor(frame_laptop, cv2.COLOR_BGR2GRAY)
    is_overexposed = np.mean(gray_frame_laptop) >= 200
    is_black = np.mean(gray_frame_laptop) <= 20

    if is_overexposed or is_black:
         sd.play(np.random.random(fs * duration), fs)  
    else:
         sd.play(np.zeros(fs * duration), fs)  


    sd.wait()

    if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        if not is_video_saving:
            output_video = cv2.VideoWriter('output_video.mp4', fourcc, 20.0, (combined_frame.shape[1], combined_frame.shape[0]))
            print('Started saving video.')
            is_video_saving = True
        else:
            output_video.release()
            output_video = None
            print('Stopped saving video.')
            is_video_saving = False

video_capture_phone.release()
video_capture_laptop.release()
cv2.destroyAllWindows()
