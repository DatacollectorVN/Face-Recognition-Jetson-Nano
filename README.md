# Face-Recognition-Jetson-Nano
This our project in Bio-Photonic class at BME - International University - VNU.

[Slide](https://docs.google.com/presentation/d/1ubix9-0_nUYJHcTf9s-gZwm7NsP12SqhFFAGRUtJUmE/edit?usp=sharing) presentation this week

# Setup requirements
## 1. Macos (M1)
### Prerequirements
+ Install [HomeBrew](https://brew.sh).
+ Install [Conda](https://docs.conda.io/en/latest/miniconda.html).

### Setup environment for dlib

```bash
brew install xquartz --cask
brew install gtk+3 boost
brew install boost-python3
brew install cmake
```
### Create virtual environment
```bash
conda create -n photonic python=3.9 -y
conda actiavte photonic
pip install -r requirements.txt
```

*Note:* In Mac M1 can create 2 python version (3.8 and 3.9), when we used python3.8 then `import dlib` in python file, we got the error `ImportError: dlopen - symbol not found in flat namespace`. But when we changed python3.9 the problems was resolved.
## 2. Jetson-Nano



