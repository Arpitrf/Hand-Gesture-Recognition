# Hand-Gesture-Recognition   ![](https://img.shields.io/github/license/mashape/apistatus.svg)

### About
An online hand gesture recognition system that facilitates interaction between a human and [Nao](https://www.thisnao.com/) robot using hand gesture recognition.<br/>
The model is a 3-D CNN (3 dimensional Convolutional Neural Network) built using Pytorch. The model has been trained on a subset of the [20-bn jester dataset](http://www.20bn.com/datasets/jester) for hand gesture recognition. The classes used and their corresponding actions performed by Nao are - 

| Action Label |      Action Performed by Nao      |
|:----------|:-------------|
| No Gesture |  Do nothing |
| Slide two fingers left |    Turn and move left by 20 cm   |
| Slide two fingers right | Turn and move right by 20 cm |
| Slide two fingers down | Sit down |
| Slide two fingers up | Stand up |
| Shaking Hand | Wave and Say Hi |
| Stop sign | Move backward by 20 cm |
| Pulling two fingers in | Move forward by 20 cm |

### Pre-requisites
  - [Python 3](https://www.python.org/download/releases/3.0/)
  - [Python 2.7](https://www.python.org/download/releases/2.7/)
  - [Pytorch](https://pytorch.org/)
  - [Naoqi](http://doc.aldebaran.com/2-1/naoqi/index.html)
  - [Anaconda](https://www.anaconda.com/) or some other virtual environment

### Description of Codes
The codes are present in the Final Codes folder in the main directory. The function of each file is as follows -
  - **server.py -** Start a server that accepts client connections and then, calls the predictor, and then returns the predicted label to the client for further action.
  - **client.py -** Start a client that connects with the server. It then reads the video frames from the camera of Nao, saves them to the directory Sample_images and informs the server that the sample has been read. It then receives the predicted label from the server and sends the corresponding action to Nao to perform.
  - **predictor.py -**  Called by server. It reads the data from the Sample_images directory and then calls the model. It finally returns the prediction to the server.
  - **model.py -** Defines the actual pytorch model used for predictions.

### How to Run
It is recommended to use [Anaconda](https://www.anaconda.com/) or some other virtual environment as the server.py runs in an environment with Python3 with Pytorch installed whereas the client.py runs in another virtual environment with Python2 and Naoqi installed since Naoqi has no release for Python3.<br />
**Note -** Run the files server.py and client.py on different terminals on the same machine. <br />
The steps for running the codes provided are - 
  - Activate environment in terminal with Python3 and Pytorch. (Considering name of environment as pytorch in case of Anaconda)
  ```
  source activate pytorch
  ```
  - Run server.py in this environment.
  ``` 
  python server.py
  ```
  - Activate the other environment in another terminal with Python2 and Naoqi. (Considering name of environment as nao in case of Anaconda)
  ```
  source activate nao
  ```
  - Run client.py in this environment. **Note -** Edit the IP of the HOST to your server IP and also change the IP of Naoqi to the IP of your Nao.
  ```
  python client.py
  ```
  - Press 'S' to start capture, perform the gesture in front of the camera and then press 'Q' to end the capture.

### Tips
  
**1. To use matplotlib in virtualenv (mac OSX) paste following in ~/.bash_profile:**

```
function frameworkpython {
    if [[ ! -z "$VIRTUAL_ENV" ]]; then
        PYTHONHOME=$VIRTUAL_ENV /usr/local/bin/python3 "$@"
    else
        /usr/local/bin/python3 "$@"
    fi
}
```

**2. TensorFlow (mac OSX):**
   - Python 3.7 does not work.
   ```
   brew unlink python
   ```
   - Install Python 3.6.5
   ```
   brew install https://raw.githubusercontent.com/Homebrew/homebrewcore/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
```

**3. Setting up Naoqi on Linux:**
  - Create a virtual environment with Python version as 2.7. In case of Anaconda - 
  ```
  conda create -n yourenvname python=2.7
  ```
  - Activate the environment.
  ```
  source activate yourenvname
  ```
  - Download Naoqi from [here](https://community.ald.softbankrobotics.com/en/dl/ZmllbGRfY29sbGVjdGlvbl9pdGVtLTEyNDEtZmllbGRfc29mdF9kbF9leHRlcm5hbF9saW5rLTAtOGVlYTk3?width=500&height=auto)<br />
  **Note -** Make sure you are using 64-bit Linux. Also, the above link is for downloading [Pepper](https://www.softbankrobotics.com/emea/en/robots/pepper) python SDK which works just as well.
  ###
  - Extract the tar file downloaded.
  ###
  - Set environment variable PYTHONPATH -
  ```
  export PYTHONPATH=${PYTHONPATH}:/path/to/python-sdk/lib/python2.7/site-packages
  ```
  - Check the installation by running python and then importing naoqi using -
  ```
  import naoqi
  ```

### Creators
  - [Arpit Bahety](https://github.com/Arpitrf)
  - [Ankur Dengla](https://github.com/ankurdengla1996)
