cmake_minimum_required(VERSION 3.1)

project(cec_core)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++2a")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(EXTRA_LIBS m)

include_directories(include)

file(GLOB_RECURSE SRC_FILES "${PROJECT_SOURCE_DIR}/src/*.c")
file(GLOB_RECURSE INC_FILES "${PROJECT_SOURCE_DIR}/include/*.h")

add_library(cecs SHARED ${SRC_FILES} ${INC_FILES})
add_executable(main main.c ${SRC_FILES} ${INC_FILES})
target_compile_options(main
  PUBLIC
  -Wall
  -fpic
  -fstack-protector-strong
  -O3
  -Wextra
  -pedantic
  -Werror
)

target_link_libraries(main ${EXTRA_LIBS} -fno-omit-frame-pointer)
