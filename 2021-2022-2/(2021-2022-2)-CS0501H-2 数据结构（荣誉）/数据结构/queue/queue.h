//
// Created by loping151 on 2022/3/8.
//

#ifndef QUEUE_QUEUE_H
#define QUEUE_QUEUE_H

template<typename elemType>
class queue
{
public:
    virtual bool isEmpty() const = 0;

    virtual void enQueue(const elemType &x) = 0;//队尾入队

    virtual elemType deQueue() = 0;//队首出列

    virtual elemType getHead() = 0;

    virtual ~queue() = default;
};

#endif //QUEUE_QUEUE_H
