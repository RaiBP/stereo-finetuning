# Stereo Fine Tuning
Dash application for tuning parameters of StereoBM and Stereo SGBM algorithms in real time.

## How to use
* Clone repository locally in `<PROJECT_PATH>`

* Install requirements with 

`pip install -r <PROJECT_PATH>/requirements.txt`

* Install necessary packages for OpenCV with

    * **Ubuntu:**  `apt-get install -y ffmpeg libsm6 libxext6`


* Execute `app.py` with

`python <PROJECT_PATH>/src/app.py`

* Open http://127.0.0.1:8050/ in browser 

* Upload left and right stereo images. They must be previously undistorted and rectified.

