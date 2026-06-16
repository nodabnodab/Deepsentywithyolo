cmake_minimum_required(VERSION 3.10)
project(deepsenty_trt_inference LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find OpenCV
find_package(OpenCV REQUIRED)
message(STATUS "OpenCV library status:")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")

# Find CUDA
find_package(CUDA REQUIRED)
include_directories(${CUDA_INCLUDE_DIRS})

# TensorRT Paths in NGC Container
set(TENSORRT_INCLUDE_DIRS "/usr/include" "/usr/include/x86_64-linux-gnu")
set(TENSORRT_LIBRARIES "/usr/lib/x86_64-linux-gnu/libnvinfer.so")

include_directories(${OpenCV_INCLUDE_DIRS} ${TENSORRT_INCLUDE_DIRS})

# Source files
file(GLOB SOURCES "src/*.cpp" "src/*.h")

add_executable(deepsenty_inference ${SOURCES})

# Target Link Libraries
target_link_libraries(deepsenty_inference PRIVATE
    ${OpenCV_LIBS}
    ${CUDA_LIBRARIES}
    ${TENSORRT_LIBRARIES}
)
