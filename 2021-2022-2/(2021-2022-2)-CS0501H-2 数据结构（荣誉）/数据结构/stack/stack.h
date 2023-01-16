//
// Created by Kailing Wang on 2022/3/3.
//

#ifndef STACK_STACK_H
#define STACK_STACK_H

template<typename element_type>
class stack
{
public:
    virtual bool isEmpty() const = 0;

    virtual void push(const element_type &x) = 0;

    virtual element_type pop() = 0;

    virtual element_type top() const = 0;

    virtual ~stack() = default;;
};

#endif //STACK_STACK_H