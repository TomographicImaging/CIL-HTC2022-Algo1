import numpy as np
from PIL import Image
import util
import os, sys

def calculate_score(path_to_our_segmentation, path_to_reference_image_png):

    img_data = Image.open(path_to_our_segmentation)
    img_arr = np.array(img_data)

    ref = util.loadImg(path_to_reference_image_png)

    return util.calcScoreArray(img_arr[:,:,0], ref)  

if __name__ == "__main__":
    score = calculate_score(os.path.abspath(sys.argv[1]),
                            os.path.abspath(sys.argv[2]))
    print ("Score: {}".format(score))