//
// Created by loping151 on 2022/2/22.
//

#include <iostream>
#include "s_link_list.h"

template<typename element_type>
typename s_link_list<element_type>::node *s_link_list<element_type>::move(int index) const
{
    node *p = head;

    while (index-- >= 0)p = p->next;
    return p;
}

template<typename element_type>
s_link_list<element_type>::s_link_list()
{
    head = new node;
    current_length = 0;
}

template<typename element_type>
void s_link_list<element_type>::clear()
{
    node *p = head->next, *q;

    head->next = nullptr;
    while (p != nullptr)//must delete all the existing nodes, or cause memory leak
    {
        q = p->next;
        delete p;
        p = q;
    }
    current_length = 0;
}

template<typename element_type>
int s_link_list<element_type>::length() const
{
    return current_length;
}

template<typename element_type>
void s_link_list<element_type>::insert(int index, const element_type &x)
{
    node *pos;

    pos = move(index - 1);//move to the previous one of index to be inserted
    pos->next = new node(x, pos->next);
    ++current_length;
}

template<typename element_type>
void s_link_list<element_type>::remove(int index)
{
    node *pos, *del;

    pos = move(index - 1);
    del = pos->next;
    pos->next = del->next;
    delete del;
    --current_length;
}

template<typename element_type>
int s_link_list<element_type>::search(const element_type &x) const
{
    node *p = head->next;
    int index = 0;

    while (p != nullptr and p->data != x)
    {
        p = p->next;
        index++;
    }
    if (p == nullptr)return -1;
    else return index;
}

template<typename element_type>
element_type s_link_list<element_type>::visit(int index) const
{
    return move(index)->data;
}

template<typename element_type>
void s_link_list<element_type>::traverse() const
{
    node *p = head->next;

    std::cout << '\n';
    while (p != nullptr)
    {
        std::cout << p->data << ' ';
        p = p->next;
    }
    std::cout << '\n';
}