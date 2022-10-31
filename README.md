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
1. Pre-processing: renormalisation, single material beam hardening correction
2. Regularised iterative reconstruction algorithm using tools from CIL: L2Norm with TV regularisation
3. Post-processing

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
