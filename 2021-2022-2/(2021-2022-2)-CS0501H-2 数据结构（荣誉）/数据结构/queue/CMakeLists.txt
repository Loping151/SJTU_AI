cmake_minimum_required(VERSION 3.21)
project(queue)

set(CMAKE_CXX_STANDARD 14)

add_executable(
        queue
        main.cpp
        queue.h
        seqQueue.cpp
        seqQueue.h
        seqQueue_withLen.cpp
        seqQueue_withLen.h
        linkQueue.cpp linkQueue.h linkQueue_withLinkedList.cpp linkQueue_withLinkedList.h)
