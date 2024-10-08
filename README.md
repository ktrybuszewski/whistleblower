# whistleblower
Software created for AEC Hackathon Wroclaw Edition 2024

Intelligent EHS (Environment, Health, and Safety) System on the Construction Site

[Challenge AEC Hackathon (4-6.10.2024) - Atlas Ward](https://atlasward.pl/aec-hackathon-wyzwania-atlas-ward/)

[AEC Hackathon Website](https://hack.creoox.com/)

[AEC Hackathon on Wroclaw University of Technology Site](https://pwr.edu.pl/uczelnia/przed-nami/aec-hackathon-wroclaw-edition-1927.html)


# Rest of the solution

[UI Part](https://github.com/mmilian/whistleblower)

[Backend and image capture part](https://github.com/gwilczura/whistleblower)


# Features

## Hardhat detection
- Detects hard hats in images and identifies their colors (white, yellow, blue).
- Fetches images through an API and processes them in real-time with camera.
- Receives and analyzes images from the camera in real time.
- Sends alerts for hard hat violations detections through an API.

## Falling detection
- Fetches images through an API and processes them in real-time with camera.
- Detects falls based on the dimensions of detected persons.
- Sends alerts about a probable fall of a person on a construction site through an API.

## People counting system
- Monitors a construction site using video feed from a camera located at the entrance.
- Counts the number of people entering and exiting the site based on their movements across defined lines.
- Updates real-time counts of individuals on the site and communicates this data via an API.
- Distinguishes between individuals entering and exiting by tracking their coordinates.
- Displays the number of people on-site in real-time on the video frame.

# Acknowledgments  
- [YOLO for the object detection algorithm](https://github.com/ultralytics/ultralytics)
- [Pre-trained to hardhat detection YOLO model](https://github.com/keremberke/awesome-yolov8-models)
- [People counting algorithm](https://github.com/noorkhokhar99/Python-OpenCV-People-Counting-with-Gmail-Alerts)



