//
// Created by Kailing Wang on 2022/3/12.
//

#include "seqQueue_withLen.h"

template<typename elemType>
void seqQueue_withLen<elemType>::doubleSpace()
{
    elemType *tmp = elem;

    elem = new elemType[2 * maxSize];
    for (int i = 0; i < maxSize; i++)
        elem[i] = tmp[(front + i + 1) % maxSize];
    front = -1;
    maxSize *= 2;

    delete[] tmp;
}

template<typename elemType>
void seqQueue_withLen<elemType>::enQueue(const elemType &x)
{
    if(length == maxSize)doubleSpace();
    int rear = (front + length + 1) % maxSize;
    elem[rear] = x;
    ++length;
}

template<typename elemType>
elemType seqQueue_withLen<elemType>::deQueue()
{
    front = (front + 1) % maxSize;
    --length;
    return elem[front];
}