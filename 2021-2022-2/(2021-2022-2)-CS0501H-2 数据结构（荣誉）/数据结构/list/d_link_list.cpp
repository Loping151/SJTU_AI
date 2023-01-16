//
// Created by loping151 on 2022/2/24.
//

#include "d_link_list.h"
#include<iostream>

template<typename element_type>
d_link_list<element_type>::d_link_list()
{
    head = new node;
    head->next = tail = new node;
    tail->prev = head;
    current_length = 0;
}

template<typename element_type>
d_link_list<element_type>::~d_link_list()
{
    clear();
    delete head, tail;
}

template<typename element_type>
int d_link_list<element_type>::length() const
{
    return current_length;
}

template<typename element_type>
typename d_link_list<element_type>::node *d_link_list<element_type>::move(int index) const
{
    node *p = head;

    while (index-- >= 0)p = p->next;
    return p;
}

template<typename element_type>
void d_link_list<element_type>::insert(int index, const element_type &x)
{
    node *pos, *tmp;

    pos = move(index);
    tmp = new node(x, pos->prev, pos);
    pos->prev->next = tmp;
    pos->prev = tmp;
    ++current_length;
}

template<typename element_type>
void d_link_list<element_type>::remove(int index)
{
    node *pos;

    pos = move(index);
    pos->prev->next = pos->next;
    pos->next->prev = pos->prev;
    delete pos;
    --current_length;
}

template<typename element_type>
void d_link_list<element_type>::clear()
{
    node *p = head->next, *q;

    head->next = tail;
    tail->prev = head;
    while (p != tail)
    {
        q = p->next;
        delete p;
        p = q;
    }
    current_length = 0;
}

template<typename element_type>
int d_link_list<element_type>::search(const element_type &x) const
{
    node *p = head->next;
    int index;

    for (index = 0; p != tail and p->data != x; ++index)p = p->next;
    if (p == tail)return -1;
    else return index;
}

template<typename element_type>
element_type d_link_list<element_type>::visit(int index) const
{
    return move(index)->data;
}

template<typename element_type>
void d_link_list<element_type>::traverse() const
{
    node *p = head->next;

    std::cout << '\n';
    while (p not_eq tail)
    {
        std::cout << p->data << ' ';
        p = p->next;
    }
    std::cout << '\n';
}