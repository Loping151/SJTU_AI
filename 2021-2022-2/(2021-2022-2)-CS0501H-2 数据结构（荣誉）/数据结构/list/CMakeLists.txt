cmake_minimum_required(VERSION 3.21)
project(list)

set(CMAKE_CXX_STANDARD 17)

add_executable(
        list
        main.cpp
        seq_list.cpp
        seq_list.h
        list.h
        s_link_list.cpp
        s_link_list.h
        d_link_list.cpp
        d_link_list.h)
