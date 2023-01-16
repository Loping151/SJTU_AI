cmake_minimum_required(VERSION 3.21)
project(stack)

set(CMAKE_CXX_STANDARD 14)

add_executable(
        stack
        main.cpp
        stack.h
        seqStack.cpp
        seqStack.h
        linkStack.cpp
        linkStack.h
        balance.cpp
        balance.h)