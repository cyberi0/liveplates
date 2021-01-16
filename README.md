# Live Plates Recognizer!! [Ubuntu 20.04](#)
Live camera feed license plate detector, based on OpenALPR.

This repo contains the standard OpenALPR build for Linux and the installed Python binding. 
As the [current OpenALPR release](https://github.com/openalpr/openalpr/releases) doesn't work out of the box with Python, some of the 
code related to the porting script (openaclr.py) was rewritten to be Python 3.7 compatible and run out-of-the-box.

This repo also features a practical implementation of the script (detection.py) to create a live video stream using 
[OpenCV](https://github.com/opencv/opencv) and detect license plates as the stream is generated. While a given license plate
is being detected, it's confidence values are summed and the most likely license plate number is registered and displayed as 
command line output of the stream. 

# Running the script:

Running from the repo base directory: 
`python3 ./detection.py`

# Required dependencies
The camera livestream requires OpenCV to be installed on the system. 

# [Installing all Dependencies - Live Plates Recognizer!!](#)
### Steps For Install Environment [Ubuntu 20.04](#)
### Step 1.  Install OpenCV
 ```sh
$ sudo apt update
$ sudo apt install libopencv-dev python3-opencv
$ python3 -c "import cv2; print(cv2.__version__)"
```

### Step 2. Install Dependences (Tesseract / Leptonica)
```sh
$ sudo apt-get update
$ sudo apt-get install libopencv-dev libtesseract-dev git cmake
$ sudo apt-get install build-essential libleptonica-dev
$ sudo apt-get install iblog4cplus-dev libcurl5-dev beanstalkd
$ sudo apt-get install curl
```

# Step 3. Installing JAVA-JDK Default JDNI
```sh
$ gedit CMakeLists.txt :: "set (CMAKE_CXX_STANDARD 11)"
$ sudo apt-get -y install beanstalkd
$ sudo apt-get install -y default-jdk
$ export JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
$ sudo apt-get update && apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev
```

# Step 4. Install CURL & OpenSSL - DEV
```sh
$ sudo -i
$ sudo apt update && sudo apt upgrade 
$ sudo apt install curl && sudo apt-get install libcurl4-openssl-dev
```

# Step 5 Clone & Install Open ALPR
```sh
$ git clone https://github.com/openalpr/openalpr.git
$ cd openalpr/src/
$ mkdir build
$ cd build/
$ cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
$ sudo make install
```

```sh
$ sudo apt-get update && sudo apt-get install python-openalpr
$ sudo apt-get update && sudo apt-get install python3-openalpr
$ sudo apt-get update && sudo apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev
$
```

### Test Library Open ALPR
```sh
$ wget http://plates.openalpr.com/ea7the.jpg
$ alpr -c us ea7the.jpg
```

#### Step 6. Binding Python
```sh
$ sudo python3 -m pip install 'python-language-server[all]'
$ sudo cp -a /usr/share/openalpr/runtime_data/ocr/tessdata/*.traineddata /usr/share/openalpr/runtime_data/ocr/
$ cd openalpr/src/bindings/python
$ python3 setup.py install
```

### Step 7. Clone Project Liveplates & Run
```sh
$ git clone git@github.com:cyberi0/liveplates.git
$ python3 ./detection.py
```

