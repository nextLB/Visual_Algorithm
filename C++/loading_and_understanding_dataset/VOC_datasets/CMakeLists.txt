cmake_minimum_required(VERSION 3.31)
project(VisualizeVOCDatasets)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)

add_executable(main main.cpp)
target_link_libraries(main ${OpenCV_LIBS})
