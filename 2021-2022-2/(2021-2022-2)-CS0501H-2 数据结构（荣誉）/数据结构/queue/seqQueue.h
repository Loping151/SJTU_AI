//
// Created by Kailing Wang on 2022/3/10.
//

#ifndef QUEUE_SEQQUEUE_H
#define QUEUE_SEQQUEUE_H

#include "queue.h"

template<typename elemType>
class seqQueue : public queue<elemType>
{
private:
    elemType *elem;
    int maxSize;
    int front, rear;

    void doubleSpace();

public:
    explicit seqQueue(int size = 10);

    ~seqQueue();

    bool isEmpty() const;

    void enQueue(const elemType &x);

    elemType deQueue();

    elemType getHead() const;
};


#endif //QUEUE_SEQQUEUE_H
