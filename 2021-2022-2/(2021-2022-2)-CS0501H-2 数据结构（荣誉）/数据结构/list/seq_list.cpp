//
// Created by loping151 on 2022/2/22.
//
#include "seq_list.h"
#include <iostream>

template<typename element_type>
seq_list<element_type>::~seq_list()
{
    delete data;
}

template<typename element_type>
void seq_list<element_type>::clear()
{
    current_length = 0;
}

template<typename element_type>
int seq_list<element_type>::length() const
{
    return current_length;
}

template<typename element_type>
element_type seq_list<element_type>::visit(int index) const
{
    return data[index];
}

template<typename element_type>
void seq_list<element_type>::traverse() const
{
    std::cout << '\n';
    for (int index = 0; index < current_length; ++index)
        std::cout << data[index] << ' ';
}

template<typename element_type>
seq_list<element_type>::seq_list(int initial_length)
{
    data = new element_type[initial_length];
    max_size = initial_length;
    current_length = 0;
}

template<typename element_type>
int seq_list<element_type>::search(const element_type &x) const
{
    int index;

    for (index = 0; index < current_length && data[index] != x; ++index);
    if (index == current_length) return -1;
    else return index;
}

template<typename element_type>
void seq_list<element_type>::double_space()
{
    element_type *tmp = data;

    max_size *= 2;
    data = new element_type[max_size];
    for (int index = 0; index < current_length; ++index)
        data[index] = tmp[index];
    delete[]tmp;
}

template<typename element_type>
void seq_list<element_type>::insert(int index, const element_type &x)
{
    if (current_length == max_size)
        double_space();
    for (int i = current_length; i > index; i--)
        data[i] = data[i - 1];
    data[index] = x;
    ++current_length;
}

template<typename element_type>
void seq_list<element_type>::remove(int index)
{
    for (int i = index; i < current_length; i++)
        data[i] = data[i + 1];
    --current_length;
}
