# Hand-Gesture-Recognition

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

### Description of Codes
The codes are present in the Final Codes folder in the main directory. The function of each file is as follows -
  - **server.py -** Start a server that accepts client connections and then, calls the predictor, and then returns the predicted label to the client for further action.
  - **client.py -** Start a client that connects with the server, then reads video frames from the camera of Nao. It then saves the data to the Sample_images directory and informs the server that the sample has been read. Then receives the predicted label from the server and sends the corresponding action to Nao to perform.
  - **predictor.py -** Reads the frames from the Sample_images directory, calls the model, and then sends the prediction to the server.
  - **model.py -** Defines the actual pytorch model used for predictions.

### Steps to Run
  - 


### Tips
  
1. To use matplotlib in virtualenv (mac OSX) paste following in ~/.bash_profile:

```
function frameworkpython {
    if [[ ! -z "$VIRTUAL_ENV" ]]; then
        PYTHONHOME=$VIRTUAL_ENV /usr/local/bin/python3 "$@"
    else
        /usr/local/bin/python3 "$@"
    fi
}
```

2. TensorFlow:
   - Python 3.7 does not work.
   - brew unlink python
   - Installs Python 3.6.5 - brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb


