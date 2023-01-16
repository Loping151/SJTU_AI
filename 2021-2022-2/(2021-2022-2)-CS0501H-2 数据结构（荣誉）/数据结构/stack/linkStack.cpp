//
// Created by Kailing Wang on 2022/3/3.
//

#include "linkStack.h"

template<typename element_type>
linkStack<element_type>::linkStack()
{
    top_p = nullptr;
}

template<typename element_type>
linkStack<element_type>::~linkStack()
{
    node *tmp;

    while (top_p != nullptr)
    {
        tmp = top_p;
        top_p = top_p->next;
        delete tmp;
    }
}

template<typename element_type>
bool linkStack<element_type>::isEmpty() const
{
    return top_p == nullptr;
}

template<typename element_type>
void linkStack<element_type>::push(const element_type &x)
{
    top_p = new node(x, top_p);
}

template<typename element_type>
element_type linkStack<element_type>::pop()
{
    node *tmp = top_p;

    element_type x = tmp->data;
    top_p = tmp->next;
    delete tmp;
    return x;
}

template<typename element_type>
element_type linkStack<element_type>::top() const
{
    return top_p->data;
}
