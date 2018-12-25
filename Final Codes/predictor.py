import cv2 
from imutils.video import VideoStream
import time
import torch
import os
import glob
from PIL import Image
from torchvision.transforms import *
import argparse
from model import ConvColumn
import torch.nn as nn
import json
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
# Function to extract frames

IMG_EXTENSIONS = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png']
gesture_dict = {
    0 : 'No Gesture',
    1 : "Slide Two Fingers Left",
    2 : "Slide Two Fingers Right",
    3 : "Slide Two Fingers Down", 
    4 : "Slide Two Fingers Up",
    5 : "Shaking Hand",
    6 : "Stop Sign",
    7 : "Pull Two Fingers In"
}

def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    #print("******")
    #print(topk)
    maxk = max(topk)
    #print(maxk)
    batch_size = target.size(0)

    _, pred = output.cpu().topk(maxk, 1, True, True)
    print(pred)
    top_pred = pred[0][0]
    print("\n---ANSWER---")
    print(gesture_dict[top_pred.item()])
    pred = pred.t()
    #print(pred)
    #print("^^^")
    #print(target.view(1, -1).expand_as(pred))
    #print("^^^")
    correct = pred.eq(target.view(1, -1).expand_as(pred))
    #print("***", correct)
    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0)
        #print(k, correct_k)
        res.append(correct_k.mul_(100.0 / batch_size))
    #return res
    gesture_label_int = [top_pred.item()]
    return gesture_label_int

def get_frame_names(path):
    nclips = 1
    is_val = False
    step_size = 2
    clip_size = 18
    frame_names = []
    for ext in IMG_EXTENSIONS:
        frame_names.extend(glob.glob(os.path.join(path, "*" + ext)))
    frame_names = list(sorted(frame_names))
    num_frames = len(frame_names)

    # set number of necessary frames
    if nclips > -1:
        num_frames_necessary = clip_size * nclips * step_size
    else:
        num_frames_necessary = num_frames

    # pick frames
    offset = 0
    #print(num_frames_necessary, num_frames)
    if num_frames_necessary > num_frames:
        # pad last frame if video is shorter than necessary
        frame_names += [frame_names[-1]] * (num_frames_necessary - num_frames)
    elif num_frames_necessary < num_frames:
        # If there are more frames, then sample starting offset
        diff = (num_frames - num_frames_necessary)
        # Temporal augmentation
        if not is_val:
            offset = np.random.randint(0, diff)
    frame_names = frame_names[offset:num_frames_necessary +
                                offset:step_size]
    return frame_names

def FrameCapture(path): 
      
    # Path to video file 
    # vidObj = cv2.VideoCapture(0) 
  
    # # Used as counter variable 
    # count = 0
  
    # # checks whether frames were extracted 
    # success = 1
    # #path = "./test_img/"
    # vs = VideoStream(src=0).start()
    # #time.sleep(2.0)
    # flag = 0
    # while success:
    #     frame = vs.read()
    #     cv2.imshow("Preview", frame)
    #     #i = i + 1
    #     key = cv2.waitKey(1) & 0xFF
    #     if key == ord("s"):
    #         flag = 1
            
    #     if flag == 1:
    #         success, image = vidObj.read() 
    #         image = cv2.resize(image,(176,100))
    #         # Saves the frames with frame-count
    #         if count < 10: 
    #             cv2.imwrite(os.path.join(path ,"0%d.jpg" % count), image)
    #         else:
    #              cv2.imwrite(os.path.join(path ,"%d.jpg" % count), image)
    #         count += 1
    #     if key == ord("q"):
    #         break

    str2bool = lambda x: (str(x).lower() == 'true')
    parser = argparse.ArgumentParser(
        description='PyTorch Jester Training using JPEG')
    parser.add_argument('--use_gpu', default=False, type=str2bool,
                        help="flag to use gpu or not.")
    parser.add_argument('--config', '-c', help='json config file path')
    parser.add_argument('--resume', '-r', default=False, type=str2bool,
                        help="resume training from given checkpoint.")
    parser.add_argument('--gpus', '-g', help="gpu ids for use.")
    args = parser.parse_args()
    device = torch.device("cuda" if args.use_gpu and torch.cuda.is_available() else "cpu")

    if args.use_gpu:
        gpus = [int(i) for i in args.gpus.split(',')]
        print("=> active GPUs: {}".format(args.gpus))

    # with open(args.config) as data_file:
    #     config = json.load(data_file)


    with open("configs/config.json") as data_file:
        config = json.load(data_file)


    transform = Compose([
            CenterCrop(84),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406],
                      std=[0.229, 0.224, 0.225])
        ])

    


    model = ConvColumn(8)

    if args.use_gpu:
            model = torch.nn.DataParallel(model, device_ids=gpus).to(device)
    #print(model)
    #if args.resume:
    if 1:
        if os.path.isfile(config['checkpoint']):
            print("=> loading checkpoint '{}'".format(args.resume))
            checkpoint = torch.load(config['checkpoint'], map_location='cpu')
            new_state_dict = OrderedDict()
            #c2 = copy.deepcopy(checkpoint)
            #print(checkpoint.items())
            for k, v in checkpoint.items():
                #print(k)
                if(k == 'state_dict'):
                    del checkpoint['state_dict']
                    #print(type(v))
                    for j, val in v.items():
                        #print(val)
                        name = j[7:] # remove `module.`
                        new_state_dict[name] = val
                    checkpoint['state_dict'] = new_state_dict
                    break;
            args.start_epoch = checkpoint['epoch']
            best_prec1 = checkpoint['best_prec1']
            model.load_state_dict(checkpoint['state_dict'])
            print("=> loaded checkpoint '{}' (epoch {})"
                      .format(config['checkpoint'], checkpoint['epoch']))
        else:
            print("=> no checkpoint found at '{}'".format(
                    config['checkpoint']))
    




    #model = load_state_dict(torch.load('../trainings/jpeg_model/jester_conv_example/checkpoint.pth.tar'))

    #print(model)
    #img_paths = get_frame_names('../Gesture_Recog_Testing/28')
    img_paths = get_frame_names('test_img')
    imgs = []
    for img_path in img_paths:
        img = Image.open(img_path).convert('RGB')
        #plt.imshow(img)
        #plt.show()
        #print(img)
        img = transform(img)
        #img = np.swapaxes(img,0,2)
        #print(img.shape)
        #plt.imshow(img)
        #plt.show()
        #print(img.shape)
        #print(torch.unsqueeze(img,0).shape)
        imgs.append(torch.unsqueeze(img, 0))

    # format data to torch
    #print(np.asarray(imgs).size())
    data = torch.cat(imgs)
    #print(data.shape)
    data = data.permute(1, 0, 2, 3)
    #print(data.shape)
    data = data[None, :, :, :, :]
    #print(data.shape)
    #print(data)
    target = [2]
    target = torch.tensor(target)
    #print(target)
    data = data.to(device)
    #target = target.to(device)

    model.eval()
    output = model(data)
    #print(output)
    print("\nOutput values for all the 8 classes: ")
    print(output.detach()) 
    gesture_label_int = accuracy(output.detach(), target.detach().cpu(), topk=(1, 5))
    #print(prec1.item(), prec5.item())
    return gesture_label_int
      
# Driver Code 
if __name__ == '__main__': 
  
    # Calling the function 
    FrameCapture("./test_img/") 