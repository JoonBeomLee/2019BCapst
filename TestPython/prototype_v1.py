import os
import sys
import cv2
import time
import numpy as np

## pose estimation
from config_reader import config_reader 
from preprocessing import extract_parts, draw
from cmu_model import get_testing_model

if __name__ == '__main__':
    # cam_type, default = "Basic"
    cam_type_state = ["Basic", "Add Skeleton", "Only Skeleton"]
    cam_type = 0
    # 운동 종류
    sports_type = "Test"
    opencv_model_path = "../../large_file/model.h5"
    
    # 파일 사이즈 축소를 위한 고정 값
    width = 320
    height = 480

    # model params init
    model = get_testing_model()
    model.load_weights(opencv_model_path)
    params, model_params = config_reader()

    scale_search = [0.22, 0.25, .5, 1, 1.5, 2]  # [.5, 1, 1.5, 2]
    scale_search = scale_search[0:1]
    params['scale_search'] = scale_search

    # cam reader
    cam = cv2.VideoCapture("./data/joonb_encoded_2.mp4")
    ret_val, orig_image = cam.read()

    # image resize
    orig_image = cv2.resize(orig_image, (width, height))
    
    # frame_text
    frame_text = sports_type

    # 캠이 켜져 있을 동안
    while(cam.isOpened() and ret_val is True):

        # generate image with body parts
        all_peaks, subset, candidate = extract_parts(orig_image, params, model, model_params)
        canvas = draw(orig_image, all_peaks, subset, candidate)

        # add remove background only skeleton
        numpy_tmp = np.zeros((canvas.shape[0], canvas.shape[1], 3), dtype=np.uint8)
        canvas_skeleton = draw(numpy_tmp, all_peaks, subset, candidate)
        canvas_skeleton_gray = cv2.cvtColor(canvas_skeleton, cv2.COLOR_BGR2GRAY) 

        # input key 
        # basic 0 | add skeleton 1 | only skeleton 2
        if (cam_type % 3 == 0): print_frame = orig_image; frame_text = cam_type_state[cam_type % 3]
        elif (cam_type % 3 == 1): print_frame = canvas; frame_text = cam_type_state[cam_type % 3]
        elif (cam_type % 3 == 2): print_frame = canvas_skeleton; frame_text = cam_type_state[cam_type % 3]

        cv2.putText(print_frame, frame_text, (480
        , 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        cv2.imshow('Prototype', print_frame)

        # 입력 키 
        # q : 종료 || space bar : 캡쳐
        input_key = cv2.waitKey(1)
        if input_key == ord('q'): break
        elif input_key == ord('t'): 
            frame_text = frame_text + str(cam_type)
            cam_type += 1

        ret_val, orig_image = cam.read()
        orig_image = cv2.resize(orig_image, (width, height))

    cam.release()
    cv2.destroyAllWindows()