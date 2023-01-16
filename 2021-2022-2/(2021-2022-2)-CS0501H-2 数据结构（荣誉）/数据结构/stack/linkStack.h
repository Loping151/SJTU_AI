//
// Created by Kailing Wang on 2022/3/3.
//

#ifndef STACK_LINKSTACK_H
#define STACK_LINKSTACK_H

#include"stack.h"

template<typename element_type>
class linkStack : public stack<element_type>
{
private:
    struct node
    {
        element_type data;
        node *next;

        explicit node(const element_type &x, node *next) : data(x), next(next) {}

        node() : next(nullptr) {}

        ~node() = default;
    };

    node *top_p;
public:
    linkStack();

    ~linkStack();

    bool isEmpty() const;

    void push(const element_type &x);

    element_type pop();

    element_type top() const;
};


#endif //STACK_LINKSTACK_H
