ECHO -- Starting OpenCV Configuration --

ECHO ---- Opening Visual Studio builder ----

call "C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Auxiliary/Build/vcvars64.bat"

ECHO ---- Setting up environment variables ----

call set_env_paths.bat

ECHO ---- Running CMake Commands ----

call "C:/Program Files/CMake/bin/cmake.exe" -B"%openCvBuild%/" -H"%openCvSource%/" -G"%generator%" -DCMAKE_BUILD_TYPE=%buildType% -DOPENCV_EXTRA_MODULES_PATH="%openCVExtraModules%/" ^
-DINSTALL_TESTS=ON -DINSTALL_C_EXAMPLES=ON -DBUILD_EXAMPLES=ON ^
-DBUILD_opencv_world=ON ^
-DWITH_CUDA=ON -DCUDA_TOOLKIT_ROOT_DIR="%toolkitRoot%" -DCUDA_FAST_MATH=ON -DWITH_CUBLAS=ON -DCUDA_ARCH_BIN=7.5 -DWITH_NVCUVID=ON ^
-DWITH_OPENGL=ON -DENABLE_FAST_MATH=ON ^
-DWITH_MFX=ON ^
-DBUILD_opencv_python3=ON -DPYTHON3_INCLUDE_DIR=%pathToAnaconda%/include -DPYTHON3_LIBRARY=%pathToAnaconda%/libs/python%pyVer%.lib -DPYTHON3_EXECUTABLE=%pathToAnaconda%/python.exe -DPYTHON3_NUMPY_INCLUDE_DIRS=%pathToAnaconda%/lib/site-packages/numpy/core/include -DPYTHON3_PACKAGES_PATH=%pathToAnaconda%/Lib/site-packages/ -DOPENCV_SKIP_PYTHON_LOADER=ON

ECHO -- OpenCV Configuration has finished, proceeding to build phase --

call "C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install

:End
PAUSE