# Transcript-ASR-Application
Testing ViStreamASR and other streaming model for transcription purposes

## About

## Setting up environment
1. Setting up ViStreamASR (temporary - would update to editable later):
- Delete the current custom version and use original ViStreamASR library from repo ```https://github.com/nguyenvulebinh/ViStreamASR``` (if your local device run fine)
```
cd ./src/libs
git clone https://github.com/nguyenvulebinh/ViStreamASR.git
cd ViStreamASR
echo "from src import *" > __init__.py

cd ..
cd ..
cd ..
```
- Have custom fixes (due to some local errors) as in the uploaded directory
2. Using Conda:
```
conda create -n transcript-demo python=3.12.7
conda activate transcript-demo
pip install requirements.txt
pip install src/libs/ViStreamASR/requirements.txt
pip install https://github.com/kpu/kenlm/archive/master.zip
```
3. Editable mod is still in development