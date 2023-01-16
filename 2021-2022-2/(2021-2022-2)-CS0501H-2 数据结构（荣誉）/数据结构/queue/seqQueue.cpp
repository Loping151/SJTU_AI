//
// Created by Kailing Wang on 2022/3/10.
//

#include "seqQueue.h"

template<typename elemType>
seqQueue<elemType>::seqQueue(int size)
{
    elem = new elemType[size];
    maxSize = size;
    front = rear = 0;
}

template<typename elemType>
seqQueue<elemType>::~seqQueue()
{
    delete[] elem;
}

template<typename elemType>
bool seqQueue<elemType>::isEmpty() const
{
    return front == rear;
}

template<typename elemType>
elemType seqQueue<elemType>::deQueue()
{
    front = (front + 1) % maxSize;
    return elem[front];
}

template<typename elemType>
elemType seqQueue<elemType>::getHead() const
{
    return elem[(front + 1) % maxSize];
}

template<typename elemType>
void seqQueue<elemType>::enQueue(const elemType &x)
{
    if ((rear + 1) % maxSize == front)doubleSpace();
    rear = (rear + 1) % maxSize;
    elem[rear] = x;
}

template<typename elemType>
void seqQueue<elemType>::doubleSpace()
{
    elemType *tmp = elem;
    elem = new elemType[2 * maxSize];
    for (int i = 1; i < maxSize; i++)
        elem[i] = tmp[(front + i) % maxSize];
    front = 0, rear = maxSize;
    maxSize *= 2;
    delete tmp;
}