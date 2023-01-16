//
// Created by Kailing Wang on 2022/3/13.
//

#ifndef QUEUE_LINKQUEUE_H
#define QUEUE_LINKQUEUE_H

#include"queue.h"

template<typename elemType>
class linkQueue : public queue<elemType>
{
private:
    struct node
    {
        elemType data;
        node *next;

        explicit node(const elemType &x, node *N = nullptr) : data(x), next(N) {}

        node() : next(nullptr) {}

        ~node() = default;
    };

    node *front, *rear;

public:
    linkQueue();

    ~linkQueue();

    bool isEmpty() const;

    void enQueue(const elemType &x);

    elemType deQueue();

    elemType getHead() const;
};


#endif //QUEUE_LINKQUEUE_H
