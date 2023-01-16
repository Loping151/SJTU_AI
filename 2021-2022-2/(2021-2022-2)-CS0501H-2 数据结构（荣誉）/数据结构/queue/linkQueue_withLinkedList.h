//
// Created by Kailing Wang on 2022/3/13.
//

#ifndef QUEUE_LINKQUEUE_WITHLINKEDLIST_H
#define QUEUE_LINKQUEUE_WITHLINKEDLIST_H

template<typename elemType>
class linkQueue_withLinkedList
{
private:
    struct node
    {
        elemType data;
        node *next;

        explicit node(const elemType &data, node *next = nullptr) : data(data), next(next) {}

        node() : next(nullptr) {}

        ~node() = default;
    };

    node *rear;

public:
    linkQueue_withLinkedList() : rear(nullptr) {}

    ~linkQueue_withLinkedList();

    bool isEmpty() const { return rear == nullptr; }

    void enQueue(const elemType &x);

    elemType deQueue();

    elemType getHead() const { return rear->next->data; }
};


#endif //QUEUE_LINKQUEUE_WITHLINKEDLIST_H
