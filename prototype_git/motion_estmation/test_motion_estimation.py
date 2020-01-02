import os
import sys
import argparse
import cv2
import time
import tensorflow
import numpy as np

from config_reader import config_reader
from preprocessing import extract_parts, draw
from cmu_model import get_testing_model

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

currentDT = time.localtime()
start_datetime = time.strftime("%m-%d-%H-%M-%S", currentDT)
start_datetime_simple = time.strftime("%m-%d", currentDT)

# 이미지 사이즈 줄이는 함수 // 전체를 가지고 하면 속도가 느려지기 때문에
def crop(image, w, f): 
    return image[:, int(w * f): int(w * (1 - f))]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', type=int, default=0, help='input video file name')
    parser.add_argument('--model', type=str, default='./ref_data/model.h5', help='path to the weights file')
    parser.add_argument('--frame_ratio', type=int, default=3, help='analyze every [n] frames')
    parser.add_argument('--process_speed', type=int, default=1,
                        help='Int 1 (fastest, lowest quality) to 4 (slowest, highest quality)')

    args = parser.parse_args()

    #video = args.video
    video = "./ref_data/train_arm_01.mp4"
    keras_weights_file = args.model
    frame_rate_ratio = args.frame_ratio
    process_speed = args.process_speed

    print('start processing...')

    # load model
    # authors of original model don't use
    # vgg normalization (subtracting mean) on input images
    model = get_testing_model()
    model.load_weights(keras_weights_file)

    # load config
    params, model_params = config_reader()

    # Video reader
    cam = cv2.VideoCapture(video)
    input_fps = cam.get(cv2.CAP_PROP_FPS)
    #cam.set(3, 240); cam.set(4, 360)

    ret_val, orig_image = cam.read()
    scale_search = [0.22, 0.25, .5, 1, 1.5, 2]
    scale_search = scale_search[0:process_speed]

    ret_val, orig_image = cam.read() #ret = 제대로 read됐는지확인하는 부울타입, orig = 실질적인 프레임단위의 이미지

    width = orig_image.shape[1]
    height = orig_image.shape[0]
    factor = 0.3
    resize_fac = 8

    params['scale_search'] = scale_search

        ### add write skeleton frame
    true_file_count = 1    
    false_file_count = 1

    
    # 날짜별 디렉토리 생성
    try:
        if not(os.path.isdir("./data/outputs_" + start_datetime_simple)):
            os.makedirs(os.path.join("./data/outputs_" + start_datetime_simple))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    
    i = 0  # default is 0
    while True:
        cv2.waitKey(10)
        if cam.isOpened() is False or ret_val is False:
            break
            
        tic = time.time()

        cropped = crop(orig_image, width, factor)
        input_image = cv2.resize(cropped, (0, 0), fx=1/resize_fac, fy=1/resize_fac, interpolation=cv2.INTER_CUBIC)        
        input_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)
        all_peaks, subset, candidate = extract_parts(input_image, params, model, model_params)
        canvas = draw(cropped, all_peaks, subset, candidate, resize_fac=resize_fac)

        
        # add remove background only skeleton
        numpy_tmp = np.zeros((canvas.shape[0], canvas.shape[1], 3), dtype=np.uint8)
        canvas_skeleton = draw(numpy_tmp, all_peaks, subset, candidate)
        canvas_skeleton_gray = cv2.cvtColor(canvas_skeleton, cv2.COLOR_BGR2GRAY)

        # print frame 
        print('Processing frame: ', i)
        toc = time.time()
        print('processing time is %.5f' % (toc - tic))

        ### video print
        cv2.imshow('frame_origin', canvas)
        cv2.imshow('frame_only_skeleton_gray', canvas_skeleton_gray)

        # 입력 키 
        # q : 종료 || space bar : 캡쳐
        input_key = cv2.waitKey(1)
        if input_key == ord('q'): break
        elif input_key == ord('y'): 
            output_skeleton_file = './data/outputs_' + start_datetime_simple + "/encoded_True" + str(true_file_count) + ".png"
            cv2.imwrite(output_skeleton_file, canvas_skeleton_gray)
            print("True File Save", output_skeleton_file)
            true_file_count += 1

        elif input_key == ord('n'): 
            output_skeleton_file = './data/outputs_' + start_datetime_simple + "/encoded_False" + str(false_file_count) + ".png"
            cv2.imwrite(output_skeleton_file, canvas_skeleton_gray)
            print("False File Save", output_skeleton_file)
            false_file_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret_val, orig_image = cam.read()

    cam.release()
    cv2.destroyAllWindows()