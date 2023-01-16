//
// Created by Kailing Wang on 2022/3/13.
//

#include "linkQueue.h"

template<typename elemType>
linkQueue<elemType>::linkQueue()
{
    front = rear = nullptr;
}

template<typename elemType>
linkQueue<elemType>::~linkQueue()
{
    node *tmp;
    while (front not_eq nullptr)
    {
        tmp = front;
        front = front->next;
        delete tmp;
    }
}

template<typename elemType>
bool linkQueue<elemType>::isEmpty() const
{
    return front == nullptr;
}

template<typename elemType>
elemType linkQueue<elemType>::getHead() const
{
    return front->data;
}

template<typename elemType>
void linkQueue<elemType>::enQueue(const elemType &x)
{
    if (rear == nullptr)
        front = rear = new node(x);
    else
        rear = rear->next = new node(x);
}

template<typename elemType>
elemType linkQueue<elemType>::deQueue()
{
    node *tmp = front;
    elemType value = front->data;
    front = front->next;
    if (front == nullptr)rear = nullptr;
    delete tmp;
    return value;
}