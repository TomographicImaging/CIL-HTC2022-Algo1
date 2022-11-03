# CIL-HTC2022-Algo1

## Authors:
- Gemma Fardell (STFC), United Kingdom
- Jakob Jorgensen (DTU), Denmark
- Laura Murgatroyd (STFC), United Kingdom
- Evangelos Papoutsellis (STFC, Finden), United Kingdom
- Edoardo Pasca (STFC), United Kingdom

Brief description of your algorithm and a mention of the competition.
## Description of the algorithm

This is an entry for the [HTC2022 competition](https://www.fips.fi/HTC2022.php).
The algorithm in `algo.py` is developed using [CIL](https://www.ccpi.ac.uk/cil), a toolkit for tomographic imaging and optimisation.
The main steps of the algorithms are:
1. Pre-processing: renormalisation, single material beam hardening correction, zero padding
2. generation of pixelwise lower and upper bound circular masks (mask is fitted to the provided data)
3. Regularised iterative reconstruction algorithm using tools from CIL: L2Norm with TV regularisation
4. Post-processing: segmentation of the reconstruction with multi-Otsu threshold

## Installation instructions

Installation instructions, including any requirements.

```
conda env create --file environment.yml
```

## Usage instructions.
Show few examples.

```
conda activate env-name
python main.py path/to/input/files path/to/output/files 3
```


## Repository content
- utils.py
- algo.py
- main.py
- environment.yml
- README.md
- recalc_score.py
- test_data
  - htc2022_ta_full_recon_fbp_seg.png
  - htc2022_ta_sparse_example.mat