from argparse import ArgumentParser
import os
import glob
import util

from cil.utilities.display import show2D
from cil.recon import FDK


def preprocess(data):
    # TODO: insert preprocessing code
    return data

def segment(data):
    # TODO: insert segmentation code
    return data

# TODO: delete this method:
def run_algo(data):
    # TO BE REPLACED BY THE ALGO
    ig = data.geometry.get_ImageGeometry()
    ig.voxel_num_x = 512
    ig.voxel_num_y = 512
    fdkfull = FDK(data, ig)
    fdkfull.set_fft_order(13)
    fdkreconfull = fdkfull.run(verbose=0)
    fdkreconfull =util.flipud_unpack(util.apply_global_threshold(fdkreconfull))
    return fdkreconfull


def main():
    parser = ArgumentParser(description= 'CIL Team Algorithm 1')
    parser.add_argument('in_folder', help='Input folder')
    parser.add_argument('out_folder', help='Output folder')
    parser.add_argument('difficulty', type=int)

    args = parser.parse_args()

    input_folder = os.path.abspath(args.in_folder)
    output_folder = os.path.abspath(args.out_folder)
    difficulty = int(args.difficulty)

    print("Input folder: ", input_folder, " Output folder: ",  output_folder, " Difficulty: ", difficulty)

    input_files = glob.glob(os.path.join(glob.escape(input_folder),"*.mat"))
    if input_files == []:
        raise Exception(f"No input files found, looking in folder '{input_folder}' for files with extension '.mat'")

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for input_file in input_files:
        # Load the data:
        data = util.load_htc2022data(input_file, dataset_name="CtDataLimited")

        data_preprocessed = preprocess(data)
        # TODO: call the algorithm, instead of run_algo
        data_recon = run_algo(data_preprocessed)
        data_segmented = segment(data_recon)

        util.write_data_to_png(data_segmented, input_file, output_folder)

        

        


if __name__ == '__main__':
    main()