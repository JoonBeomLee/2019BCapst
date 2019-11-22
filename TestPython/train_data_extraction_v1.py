import os
import sys
import argparse
import cv2
import time
import numpy as np
from config_reader import config_reader

from preprocessing import extract_parts, draw

from cmu_model import get_testing_model

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

currentDT = time.localtime()
start_datetime = time.strftime("%m-%d-%H-%M-%S", currentDT)
start_datetime_simple = time.strftime("%m-%d", currentDT)

# image 사이즈 조정 -> 연산 속도 위함
def crop(image, w, f):
    #return image[:, int(w * f): int(w * (1 - f))]
    return image

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=int, default=0, help='ID of the device to open')
    parser.add_argument('--input', type=str, required=True, help='Input file path')
    parser.add_argument('--model', type=str, default='../../large_file/model.h5', help='path to the weights file')
    parser.add_argument('--frame_ratio', type=int, default=7, help='analyze every [n] frames')
    # --process_speed changes at how many times the model analyzes each frame at a different scale
    parser.add_argument('--process_speed', type=int, default=1,
                        help='Int 1 (fastest, lowest quality) to 4 (slowest, highest quality)')
    parser.add_argument('--out_name', type=str, default=None, help='name of the output file to write')

    args = parser.parse_args()
    device = args.device
    keras_weights_file = args.model
    frame_rate_ratio = args.frame_ratio
    process_speed = args.process_speed
    input_file = args.input
    out_name = args.out_name

    print('start processing...')

    # load model
    # authors of original model don't use
    # vgg normalization (subtracting mean) on input images
    model = get_testing_model()
    model.load_weights(keras_weights_file)

    # load config
    params, model_params = config_reader()

    # Video reader
    cam = cv2.VideoCapture(input_file)

    # CV_CAP_PROP_FPS
    input_fps = cam.get(cv2.CAP_PROP_FPS)
    print("Running at {} fps.".format(input_fps))

    ret_val, orig_image = cam.read()

    # 파일 사이즈 축소를 위한 고정 값
    width = 320
    height = 480
    factor = 0.3

    # input text 초기화
    input_str = ""

    orig_image = cv2.resize(orig_image, (width, height))

    print(width, height)

    scale_search = [0.22, 0.25, .5, 1, 1.5, 2]  # [.5, 1, 1.5, 2]
    scale_search = scale_search[0:process_speed]

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

    while(cam.isOpened()) and ret_val is True:

        if cam.isOpened() is False or ret_val is False:
            break

        # generate image with body parts
        all_peaks, subset, candidate = extract_parts(orig_image, params, model, model_params)
        canvas = draw(orig_image, all_peaks, subset, candidate)

        # add remove background only skeleton
        numpy_tmp = np.zeros((canvas.shape[0], canvas.shape[1], 3), dtype=np.uint8)
        canvas_skeleton = draw(numpy_tmp, all_peaks, subset, candidate)
        canvas_skeleton_gray = cv2.cvtColor(canvas_skeleton, cv2.COLOR_BGR2GRAY)

        print("orig_image : ", orig_image.shape, "canvas_skeleton : ", canvas_skeleton.shape, "canvas_skeleton_gray : ", canvas_skeleton_gray.shape)

        ## putText테스트
        #           출력 대상, 출력 문, 위치,      폰트,                         문자 크기, 문자 색상
        cv2.putText(canvas, input_str, (0, 100), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))

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
        
        # 자막 테스트
        elif input_key == ord('t'): 
            input_str = "change text"


        ret_val, orig_image = cam.read()
        orig_image = cv2.resize(orig_image, (width, height))


    cam.release()
    cv2.destroyAllWindows()
