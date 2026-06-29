cmake_minimum_required(VERSION 3.31)
project(VisualizeVOCDatasets)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


find_package(OpenCV REQUIRED)
find_package(TinyXML2 REQUIRED)



add_executable(main main.cpp)


target_link_libraries(main
    ${OpenCV_LIBS}
    tinyxml2::tinyxml2
)


