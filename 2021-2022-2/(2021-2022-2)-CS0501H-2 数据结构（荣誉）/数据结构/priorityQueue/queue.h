//
// Created by Kailing Wang on 2022/4/11.
//

#pragma once

template<typename elemType>
class queue
{
public:
    virtual ~queue() = default;

    virtual bool empty() const = 0;

    virtual void enQueue(const elemType &element) = 0;

    virtual elemType deQueue() = 0;

    virtual elemType top() const = 0;

    virtual void clear() = 0;
};