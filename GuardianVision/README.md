# Smart Security Camera System

The Smart Security Camera System is a Python-based project that utilizes computer vision and various technologies to enhance home security. The system can detect unrecognized persons in the camera's field of view, send alerts to the owner, and provide video streaming capabilities. It incorporates features such as facial recognition, real-time alerting via Twilio, and audio feedback.

## Features

- Real-time video streaming from an IP webcam and laptop camera.
- Facial recognition to identify known individuals and detect unrecognized persons.
- Twilio integration for sending alerts to the owner in case of unrecognized persons.
- Audio feedback system to play sounds based on camera exposure levels.
- Video recording capability with the ability to start and stop video recording.

## Requirements

- Python 3.6 or later
- OpenCV (`cv2`)
- face_recognition library
- Twilio API (`twilio.rest`)
- NumPy
- sounddevice
- geopy

## Getting Started

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Update the Twilio API credentials and phone numbers in the code (`account_sid`, `auth_token`, `twilio_phone_number`, `owner_phone_number`, `police_phone_number`).
4. Configure the IP webcam URL (`ip_webcam_url`) if using an IP webcam.
5. Run the Python script using `python smart_security_camera.py`.

## Usage

- The system will continuously process video feeds, detecting unrecognized persons and alerting the owner via SMS through Twilio.
- Press 'q' to exit the video display.
- Press 's' to start and stop video recording (saved as `output_video.mp4`).

## Contributing

Contributions to this project are welcome! If you find issues, have ideas for improvements, or want to add new features, please feel free to submit pull requests or open issues.


## Contact

For questions or inquiries, please contact Kishan Jai Soorya N (mail to:kishanjaisoorya16@gmail.com).
