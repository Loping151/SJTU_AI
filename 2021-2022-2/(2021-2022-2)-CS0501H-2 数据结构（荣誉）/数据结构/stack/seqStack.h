//
// Created by Kailing Wang on 2022/3/3.
//

#ifndef STACK_SEQSTACK_H
#define STACK_SEQSTACK_H

#include"stack.h"

template<typename element_type>
class seqStack : public stack<element_type>
{
private:
    element_type *elem;
    int top_p;
    int maxSize;

    void doubleSpace();

public:
    explicit seqStack(int initSize = 10);

    ~seqStack();

    bool isEmpty() const;

    void push(const element_type &x);

    element_type pop();

    element_type top() const;
};

#endif //STACK_SEQSTACK_H
