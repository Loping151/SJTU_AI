//
// Created by Kailing Wang on 2022/4/11.
//

#pragma once

#include"queue.h"
#include<cstdio>

template<typename elemType>
class Less
{
public:
    bool operator()(const elemType &left, const elemType &right) const
    {
        return left < right;
    }
};

template<typename elemType>
class Greater
{
public:
    bool operator()(const elemType &left, const elemType &right) const
    {
        return left > right;
    }
};

template<typename elemType, typename compareRule = Less<elemType>>
class priorityQueue : public queue<elemType>
{
private:
    elemType *data;
    int currentLength, maxSize;
    compareRule compare;

    void doubleSpace();

    void update(int current);

    void construct();

public:
    explicit priorityQueue(int size = 100);

    priorityQueue(const elemType input[], int size);

    ~priorityQueue();

    bool empty() const;

    void enQueue(const elemType &element);

    elemType deQueue();

    elemType top() const;

    void clear();
};

template<typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::doubleSpace()
{
    elemType *tempData = data;
    maxSize <<= 1;
    data = new elemType[maxSize + 1];
    for (int i = 0; i <= currentLength; i++)
        data[i] = tempData[i];
    delete[] tempData;
}

template<typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::update(int current)
{
    elemType temp = data[current];
    for (int next; (current << 1) <= currentLength; current = next)
    {
        next = current << 1;
        if (next != currentLength && compare(data[next | 1], data[next]))
            next |= 1;
        if (!compare(data[next], temp))
            break;
        data[current] = data[next];
    }
    data[current] = temp;
}

template<typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::construct()
{
    for (int i = currentLength >> 1; i; i--)
        update(i);
}

template<typename elemType, typename compareRule>
priorityQueue<elemType, compareRule>::priorityQueue(int size) : currentLength(0), maxSize(size)
{
    data = new elemType[size];
}

template<typename elemType, typename compareRule>
priorityQueue<elemType, compareRule>::priorityQueue(const elemType input[], int size) : currentLength(size),
                                                                                          maxSize(size + 10)
{
    data = new elemType[maxSize];
    for (int i = 0; i < size; i++)
        data[i + 1] = input[i];
    construct();
}

template<typename elemType, typename compareRule>
priorityQueue<elemType, compareRule>::~priorityQueue()
{
    delete[] data;
}

template<typename elemType, typename compareRule>
bool priorityQueue<elemType, compareRule>::empty() const
{
    return currentLength == 0;
}

template<typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::enQueue(const elemType &element)
{
    if (currentLength == maxSize - 1)
        doubleSpace();
    int current = ++currentLength;
    while (current > 1 && compare(element, data[current >> 1]))
        data[current] = data[current >> 1], current >>= 1;
    data[current] = element;
}

template<typename elemType, typename compareRule>
elemType priorityQueue<elemType, compareRule>::deQueue()
{
    if (!currentLength)
        printf("Error: Heap is already empty");
    elemType result = data[1];
    data[1] = data[currentLength--];
    update(1);
    return result;
}

template<typename elemType, typename compareRule>
elemType priorityQueue<elemType, compareRule>::top() const
{
    return data[1];
}

template<typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::clear()
{
    currentLength = 0;
}