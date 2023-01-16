//
// Created by Kailing Wang on 2022/3/17.
//

#ifndef TREE_BTREE_H
#define TREE_BTREE_H

template<typename elemType>
class bTree
{
public:
    virtual void clear() = 0;

    virtual bool isEmpty() const = 0;

    virtual elemType Root(elemType flag) const = 0;

    virtual elemType parent(elemType x, elemType flag) const = 0;

    virtual elemType lchild(elemType x, elemType flag) const = 0;

    virtual elemType rchild(elemType x, elemType flag) const = 0;

    virtual void delLeft(elemType x) = 0;

    virtual void delRight(elemType x) = 0;

    virtual void preOrder() const = 0;

    virtual void midOrder() const = 0;

    virtual void postOrder() const = 0;

    virtual void levelOrder() const = 0;
};

#endif //TREE_BTREE_H
