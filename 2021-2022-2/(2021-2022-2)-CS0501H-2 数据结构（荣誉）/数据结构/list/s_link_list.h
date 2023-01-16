//
// Created by loping151 on 2022/2/22.
//

#ifndef S_LINK_LIST_S_LINK_LIST_H
#define S_LINK_LIST_S_LINK_LIST_H

#include "list.h"

template<typename element_type>
class s_link_list : public list<element_type>
{
private:
    struct node
    {
        element_type data;
        node *next;

        explicit node(const element_type &x, node *n = nullptr) : data(x), next(n) {}

        node() : next(nullptr) {}

        ~node() = default;
    };

    node *head;//no data should be stored here
    int current_length;

    node *move(int index) const;//move to the nth node, meaning that move n+1 steps from head

public:
    s_link_list();

    ~s_link_list()
    {
        clear();
        delete head;
    }

    void clear();

    [[nodiscard]] int length() const;

    void insert(int index, const element_type &x);

    void remove(int i);

    int search(const element_type &x) const;

    element_type visit(int i) const;

    void traverse() const;
};

#endif //S_LINK_LIST_S_LINK_LIST_H
