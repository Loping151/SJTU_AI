//
// Created by Kailing Wang on 2022/3/17.
//

#ifndef TREE_BINARYTREE_H
#define TREE_BINARYTREE_H

#include"bTree.h"

char default_flag = '@';

template<typename elemType>
struct Node
{
    Node *left, *right;
    elemType data;

    Node() : left(nullptr), right(nullptr) {}

    explicit Node(elemType item, Node *L = nullptr, Node *R = nullptr) : data(item), left(L), right(R) {}

    ~Node() = default;
};

template<typename elemType>
class binaryTree : public bTree<elemType>
{
    friend void printTree(const binaryTree &t, elemType flag);

    Node<elemType> *root;

public:
    binaryTree() : root(nullptr) {}

    explicit binaryTree(elemType x) : root(new Node<elemType>(x)) {}

    ~binaryTree();

    void clear();

    bool isEmpty() const;

    elemType Root(elemType flag = default_flag) const;

    elemType lchild(elemType x, elemType flag = default_flag) const;

    elemType rchild(elemType x, elemType flag = default_flag) const;

    void delLeft(elemType x);

    void delRight(elemType x);

    void preOrder() const;

    void midOrder() const;

    void postOrder() const;

    void levelOrder() const;

    void createTree(elemType flag = default_flag);

    Node<elemType>* trace(elemType x, Node<elemType>* t) const;

    elemType parent(elemType x, elemType flag = default_flag) const;
private:
    Node<elemType> *find(elemType x, Node<elemType> *T) const;

    void clear(Node<elemType> *&t);//指针的引用，方便递归的时候修改指针

    void preOrder(Node<elemType> *t) const;

    void midOrder(Node<elemType> *t) const;

    void postOrder(Node<elemType> *t) const;
};


#endif //TREE_BINARYTREE_H
