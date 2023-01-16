//
// Created by Kailing Wang on 2022/3/3.
//

#include "seqStack.h"

template<typename element_type>
seqStack<element_type>::seqStack(int initSize)
{
    elem = new element_type[initSize];
    maxSize = initSize;
    top_p = -1;
}

template<typename element_type>
seqStack<element_type>::~seqStack()
{
    delete[] elem;
}

template<typename element_type>
bool seqStack<element_type>::isEmpty() const
{
    return top_p == -1;
}

template<typename element_type>
void seqStack<element_type>::push(const element_type &x)
{
    if (top_p == maxSize - 1)doubleSpace();
    elem[++top_p] = x;
}

template<typename element_type>
element_type seqStack<element_type>::pop()
{
    return elem[top_p--];
}

template<typename element_type>
element_type seqStack<element_type>::top() const
{
    return elem[top_p];
}

template<typename element_type>
void seqStack<element_type>::doubleSpace()
{
    element_type *tmp = elem;

    elem = new element_type[2 * maxSize];

    for (int i = 0; i < maxSize; i++)
        elem[i] = tmp[i];
    maxSize *= 2;
    delete[] elem;
}