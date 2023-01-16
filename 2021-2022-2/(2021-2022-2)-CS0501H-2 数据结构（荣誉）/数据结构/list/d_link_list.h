//
// Created by loping151 on 2022/2/24.
//

#ifndef LINEAR_LIST_D_LINK_LIST_H
#define LINEAR_LIST_D_LINK_LIST_H

#include "list.h"

template<typename element_type>
class d_link_list : public list<element_type>
{
private:
    struct node
    {
        element_type data;
        node *prev, *next;

        explicit node(const element_type &x, node *p = nullptr, node *n = nullptr) : data(x), prev(p), next(n) {}

        node() : next(nullptr), prev(nullptr) {}

        ~node() = default;
    };

    node *head, *tail;
    int current_length;

    node *move(int index) const;

public:

    d_link_list();

    ~d_link_list();

    void clear();

    int length() const;

    void insert(int index, const element_type &x);

    void remove(int index);

    int search(const element_type &x) const;

    element_type visit(int index) const;

    void traverse() const;

};

#endif //LINEAR_LIST_D_LINK_LIST_H
