# basic imports
from argparse import ArgumentParser
import os
import glob
import numpy as np
# method imports
import util
from algo import pdhg_tv

def preprocess(data):
    '''Preprocess the data'''
    # renormalise data
    data_renorm = util.correct_normalisation(data)
    # pad data
    data_pad = util.pad_zeros(data_renorm)
    # apply beam hardening correction
    data_BHC = util.apply_BHC(data_pad)
    return data_BHC

def segment(data, segment_type):
    '''Run segmentation on data with method segment_type'''
    if segment_type == 1:
        ss = util.apply_global_threshold(data)
    elif segment_type == 2:
        ss = util.apply_crazy_threshold(data)
    return util.flipud_unpack(ss)
 
def create_lb_ub(data, ig, ub_mask_type, lb_mask_type, ub_val, lb_val, basic_mask_radius, lb_inner_radius):
    # create default lower bound mask
    lb = ig.allocate(0.0)
    # create upper bound mask
    if ub_mask_type == 1:
        ub = ig.allocate(ub_val)
        ub = util.apply_circular_mask(ub, basic_mask_radius)
    elif ub_mask_type == 2:
        # sample mask with upper bound to acrylic attenuation
        ub = ig.allocate(0)
        circle_parameters = util.find_circle_parameters(data, ig)
        util.fill_circular_mask(circle_parameters, ub.array, \
            ub_val, *ub.shape)
        # create lower bound mask annulus if needed
        if lb_mask_type == 1:
            inner_circle_parameters = circle_parameters.copy()
            inner_circle_parameters[0] = lb_inner_radius
            util.fill_circular_mask(circle_parameters, lb.array, lb_val, *ub.shape)
            inner = ig.allocate(0.0)
            util.fill_circular_mask(inner_circle_parameters, inner.array, 1.0, *ub.shape)
            lb.array[inner.array.astype(bool)==1.0] = 0.0

    return lb, ub


def main():
    parser = ArgumentParser(description= 'CIL Team Algorithm 1')
    parser.add_argument('in_folder', help='Input folder, containing FULL data')
    parser.add_argument('out_folder', help='Output folder, where PNGs will be written')
    parser.add_argument('difficulty', type=int)
    parser.add_argument('-omega', type=float, help="Omega. If not set, defaults to 90/ang_range")
    parser.add_argument('-alpha', type=float, help= "Alpha. This is required.")
    parser.add_argument('-ang_start', type=int, help="Starting angle, degrees. This is required.")
    parser.add_argument('-ang_range', type=int, help="Angular range, degrees. This is required.")

    args = parser.parse_args()

    input_folder = os.path.abspath(args.in_folder)
    output_folder = os.path.abspath(args.out_folder)
    difficulty = int(args.difficulty)
    alpha = args.alpha
    if alpha is None:
        raise Exception("-alpha must be set!")
    ang_range = args.ang_range
    if ang_range is None:
        raise Exception("-ang_range must be set!")
    ang_start = args.ang_start
    if ang_start is None:
        raise Exception("-ang_start must be set!")
    omega = args.omega
    if omega is None:
        omega = 90.0/ang_range

    print("Input folder: ", input_folder, " Output folder: ",  output_folder, " Difficulty: ", difficulty)
    print("Omega: ", omega, "Alpha: ", alpha, "Ang Start: ", ang_start, "Ang Range: ", ang_range)

    ###########################################################
    # CONFIGURATION
    # Image size
    im_size = 512

    # Upper bound mask
    ub_val = 0.040859 # acrylic_attenuation in unit 1/mm
    ub_mask_type = 2   # 1 basic 0.97 circle. 2 fitted
    basic_mask_radius = 0.97

    # Lower bound mask
    lb_mask_type = 0   # 0:  lower bound 0 everywhere, 1: outer annulus equal to upper bound acrylic
    lb_inner_radius = 200
    lb_val = ub_val  # could be changed to 0.04 or other smaller values

    # Reconstruction
    num_iters = 2000
    # with this algo we do not change alpha with difficulty level
    update_objective_interval = 100
    verbose = 1
    
    # Segmentation
    segmentation_method = 2  # 1 basic thresholding, 2 crazy

    #####################################################


    input_files = glob.glob(os.path.join(glob.escape(input_folder),"*.mat"))
    if input_files == []:
        raise Exception(f"No input files found, looking in folder '{input_folder}' for files with extension '.mat'")

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)


    # MAIN FOR LOOP TO PROCESS EACH FILE IN THE INPUT DIRECTORY
    for input_file in input_files:
        # Load the data:
        datafull = util.load_htc2022data(input_file, dataset_name="CtDataFull")
        data = util.generate_reduced_data(datafull, ang_start, ang_range)
        print(datafull)
        print(data)
        # Preprocess
        data_preprocessed = preprocess(data)
        # discover angular range
        

        ig = data_preprocessed.geometry.get_ImageGeometry()
        ig.voxel_num_x = im_size
        ig.voxel_num_y = im_size

        # NOTE: the fit of the sample mask works best with the non pre-processed data
        # as the FDK reconstruction is more blurry!!!
        lb, ub = create_lb_ub(data, ig, ub_mask_type, lb_mask_type, 
                                ub_val, lb_val, basic_mask_radius, lb_inner_radius)
        
        
        # algorithmic parameters
        args = [omega, alpha]
        
        # Run reconstruction
        data_recon = pdhg_tv(data_preprocessed, ig, lb, ub, *args, num_iters=num_iters, 
                update_objective_interval=update_objective_interval, verbose=verbose)
        
        data_segmented = segment(data_recon, segmentation_method)

        util.write_data_to_png(data_segmented, input_file, output_folder)

    print("Omega: ", omega, "Alpha: ", alpha, "Ang Start: ", ang_start, "Ang Range: ", ang_range)

    return 0

if __name__ == '__main__':
    ret = main()
    exit(ret)