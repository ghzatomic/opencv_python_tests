sudo apt install python3-opencv libopencv-dev

mkdir content
cd content
git clone https://github.com/roboflow-ai/darknet.git

./copy_arquivos_treinamento_darknet.sh

python darknet_generate_config.py

./exec_treinamento_darknet.sh





Step 0: Prerequisites

    Download and install CUDA and cuDNN as explained here.
    https://developer.nvidia.com/cuda-downloads
    https://developer.nvidia.com/rdp/cudnn-download
    Download and install CmakeGUI from here.
    https://cmake.org/
    Download and install Visual Studio Community Edition from here. Install with Desktop Development for C++ option.
    https://visualstudio.microsoft.com/pt-br/thank-you-downloading-visual-studio/?sku=Community&rel=16

    Download OpenCV source from here.
    https://github.com/opencv/opencv/archive/4.4.0.zip
    Download OpenCV contrib from here. Make sure the version matches with OpenCV.
    https://github.com/opencv/opencv_contrib/archive/4.4.0.zip
    Extract OpenCV and OpenCV contrib zip files.
    Make an empty folder called build

Step 1: Building OpenCV using CMake GUI

    Open CMake GUI and browse for OpenCV source folder.
    Browse for make folder that we created above.
    Click on Configure and select X64 platform and hit Finish.
    New options will appear in CMake in red color. Tick these checkboxes there: WITH_CUDA, OPENCV_DNN_CUDA, ENABLE_FAST_MATH
    On the same window, go to OPENCV_EXTRA_MODULES_PATH and browse for OpenCV contrib directory and point to the modules subfolder.
    Hit Configure again. You will see new options in red color. Tick CUDA_FAST_MATH checkbox. From CUDA_ARCH_BIN property, remove any compute architecture that your model of nVidia GPU does not support. You can find a list of compatible compute architectures for your model of GPU here.
    Hit Configure and then Generate.

Step 2: Making OpenCV with Visual Studio

    Go to build folder and open OpenCV.sln file with Visual Studio.
    Once opened, change Debug to Release from the top.
    On the panel at the right-hand side, expand Cmake Targets.
    Right-click on ALL_BUILD and click on build.
    Once done, right-click on Install and click on build.

https://jordanbenge.medium.com/anaconda3-opencv-with-cuda-gpu-support-for-windows-10-e038569e228


cmake --build D:\git\opencv\build --target install --config release