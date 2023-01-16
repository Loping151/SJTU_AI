cmake_minimum_required(VERSION 3.21)
project(priorityQueue)

set(CMAKE_CXX_STANDARD 14)

add_executable(
        main
        main.cpp
        priorityQueue.h
        queue.h
)
