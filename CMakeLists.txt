cmake_minimum_required(VERSION 3.22)

project(cec_test)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(EXTERNAL_DIR "/home/ian/IOHexperimenter/external")

include_directories(${EXTERNAL_DIR}/fmt/include/)
include_directories(${EXTERNAL_DIR}/clutchlog)
include_directories(${EXTERNAL_DIR}/json/include)

find_package(ioh REQUIRED)

add_executable(cec_test main.cpp)
target_link_libraries(cec_test ioh::ioh)

add_executable(rotation_matrix rotation_matrix.cpp)
target_link_libraries(rotation_matrix ioh::ioh)