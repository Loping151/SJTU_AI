cmake_minimum_required(VERSION 3.21)
project(set)

set(CMAKE_CXX_STANDARD 14)

add_executable(set main.cpp set.h staticSet.h dynamicSet.h binarySearchTree.h AVLTree.h)
