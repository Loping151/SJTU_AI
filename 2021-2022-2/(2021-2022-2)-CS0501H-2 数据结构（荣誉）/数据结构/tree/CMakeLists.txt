cmake_minimum_required(VERSION 3.21)
project(tree)

set(CMAKE_CXX_STANDARD 14)

add_executable(
        tree
        main.cpp
        tree.h
        bTree.h
        binaryTree.cpp
        binaryTree.h
        queue.h
        linkQueue.h
        linkQueue.cpp)
