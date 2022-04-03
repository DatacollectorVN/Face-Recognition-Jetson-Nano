# Face-Recognition-Jetson-Nano
This our project in Bio-Photonic class at **BME - International University - VNU**.

## Setup requirements
### 1. Macos (M1)
#### Prerequirements
+ Install [HomeBrew](https://brew.sh).
+ Install [Conda](https://docs.conda.io/en/latest/miniconda.html).

#### Setup environment for dlib

```bash
brew install xquartz --cask
brew install gtk+3 boost
brew install boost-python3
brew install cmake
```
#### Create virtual environment
```bash
conda create -n photonic python=3.9 -y
conda actiavte photonic
pip install -r requirements.txt
```

*Note:* In Mac M1 can create 2 python version (3.8 and 3.9), when we used python3.8 then `import dlib` in python file, we got the error `ImportError: dlopen - symbol not found in flat namespace`. But when we changed python3.9 the problems was resolved.

### 2. Linux (Ubuntu 18.04)
#### Setup environment for dlib
```bash
sudo apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*
```
*Note:* If packages that you got before you don't need to install.

#### Create virtual environment
```bash
conda create -n photonic python=3.9 -y
conda actiavte photonic
pip install -r requirements.txt
```

### 3. Windows
#### Create virtual environment
```bash
conda create -n photonic python=3.9 -y
conda actiavte photonic
```

#### Install dlib and requirement packages
If cmake is not installed then first install it using following command
```bash
pip install cmake
```
And then install dlib and requirements
```bash
conda install -c conda-forge dlib 
pip install -r  requirements.txt
```
