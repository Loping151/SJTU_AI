//
// Created by Kailing Wang on 2022/3/13.
//

#include "linkQueue_withLinkedList.h"

template<typename elementType>
linkQueue_withLinkedList<elementType>::~linkQueue_withLinkedList()
{
    node *tmp, *delp;

    if (rear == nullptr)return;
    delp = rear->next;
    rear->next = nullptr;
    while (delp not_eq nullptr)
    {
        tmp = delp;
        delp = delp->next;
        delete tmp;
    }
}

template<typename elemType>
void linkQueue_withLinkedList<elemType>::enQueue(const elemType &x)
{
    if (rear == nullptr)
    {
        rear = new node(x);
        rear->next = rear;
    }
    else
        rear = rear->next = new node(x, rear->next);
}

template<typename elemType>
elemType linkQueue_withLinkedList<elemType>::deQueue()
{
    node *tmp = rear->next;
    elemType value = tmp->data;
    if (rear == tmp) rear = nullptr;
    else rear->next = tmp->next;
    delete tmp;
    return value;
}