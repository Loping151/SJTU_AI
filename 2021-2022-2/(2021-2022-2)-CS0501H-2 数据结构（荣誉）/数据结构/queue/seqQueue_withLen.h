//
// Created by Kailing Wang on 2022/3/12.
//

#ifndef QUEUE_SEQQUEUE_WITHLEN_H
#define QUEUE_SEQQUEUE_WITHLEN_H

template<typename elemType>
class seqQueue_withLen
{
private:
    elemType *elem;
    int maxSize;
    int front;
    int length;

    void doubleSpace();

public:
    explicit seqQueue_withLen(int size = 10) : elem(new elemType[size]), maxSize(size), front(-1), length(0) {}

    ~seqQueue_withLen() { delete[]elem; }

    bool isEmpty() const { return length == 0; }

    void enQueue(const elemType &x);

    elemType deQueue();

    elemType getHead() const { return elem[(front + 1)] % maxSize; }
};


#endif //QUEUE_SEQQUEUE_WITHLEN_H
