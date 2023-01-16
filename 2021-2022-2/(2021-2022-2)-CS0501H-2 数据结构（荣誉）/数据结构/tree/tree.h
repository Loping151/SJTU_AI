//
// Created by Kailing Wang on 2022/3/17.
//

#ifndef TREE_TREE_H
#define TREE_TREE_H

template<typename elemType>
class tree
{
public:
    virtual void clear() = 0;

    virtual bool isEmpty() const = 0;

    virtual elemType root(elemType flag) const = 0;

    virtual elemType parent(elemType x, elemType flag) const = 0;

    virtual elemType child(elemType x, int i, elemType flag) const = 0;

    virtual void remove(elemType x, int i) = 0;

    virtual void traverse() const = 0;
};

#endif //TREE_TREE_H
