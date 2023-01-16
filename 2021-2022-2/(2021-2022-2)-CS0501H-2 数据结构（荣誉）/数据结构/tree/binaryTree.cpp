//
// Created by Kailing Wang on 2022/3/17.
//

#include"binaryTree.h"
#include"linkQueue.h"
#include<iostream>

template<typename elemType>
bool binaryTree<elemType>::isEmpty() const
{
    return root == nullptr;
}

template<typename elemType>
elemType binaryTree<elemType>::Root(elemType flag) const
{
    if (root == nullptr) return flag;
    else return root->data;
}

template<typename elemType>
void binaryTree<elemType>::clear(Node<elemType> *&t)
{
    if (t == nullptr) return;
    clear(t->left);
    clear(t->right);
    delete t;
    t = nullptr;
}

template<typename elemType>
void binaryTree<elemType>::clear()
{
    clear(root);
}

template<typename elemType>
binaryTree<elemType>::~binaryTree()
{
    clear(root);
}

template<typename elemType>
void binaryTree<elemType>::preOrder(Node<elemType> *t) const
{
    if (t == nullptr) return;
    std::cout << t->data << ' ';
    preOrder(t->left);
    preOrder(t->right);
}

template<typename elemType>
void binaryTree<elemType>::preOrder() const
{
    preOrder(root);
}

template<typename elemType>
void binaryTree<elemType>::postOrder(Node<elemType> *t) const
{
    if (t == nullptr) return;
    postOrder(t->left);
    postOrder(t->right);
    std::cout << t->data << ' ';
}

template<typename elemType>
void binaryTree<elemType>::postOrder() const
{
    postOrder(root);
}

template<typename elemType>
void binaryTree<elemType>::midOrder(Node<elemType> *t) const
{
    if (t == nullptr) return;
    midOrder(t->left);
    std::cout << t->data;
    midOrder(t->right);
}

template<typename elemType>
void binaryTree<elemType>::midOrder() const
{
    midOrder(root);
}

template<typename elemType>
void binaryTree<elemType>::levelOrder() const
{
    linkQueue<Node<elemType> *> que;
    Node<elemType> *tmp;

    que.enqueue(root);

    while (not que.isEmpty())
    {
        tmp = que.dequeue();
        std::cout << tmp->data << ' ';
        if (tmp->left)que.enQueue(tmp->left);
        if (tmp->right)que.enQueue(tmp->right);
    }
}

template<typename elemType>
Node<elemType> *binaryTree<elemType>::find(elemType x, Node<elemType> *t) const
{
    Node<elemType> *tmp;
    if (t == nullptr) return nullptr;
    if (t->data == x) return t;
    if ((tmp = find(x, t->left))) return tmp;
    else return find(tmp->right);
}

template<typename elemType>
void binaryTree<elemType>::delLeft(elemType x)
{
    Node<elemType> *tmp = fine(x, root);
    if (tmp == nullptr) return;
    clear(tmp->left);
}

template<typename elemType>
void binaryTree<elemType>::delRight(elemType x)
{
    Node<elemType> *tmp = fine(x, root);
    if (tmp == nullptr) return;
    clear(tmp->right);
}

template<typename elemType>
elemType binaryTree<elemType>::lchild(elemType x, elemType flag) const
{
    Node<elemType> *tmp = find(x, root);
    if (tmp == nullptr or tmp->left == nullptr) return flag;

    return tmp->left->data;
}

template<typename elemType>
elemType binaryTree<elemType>::rchild(elemType x, elemType flag) const
{
    Node<elemType> *tmp = find(x, root);
    if (tmp == nullptr or tmp->right == nullptr) return flag;

    return tmp->right->data;
}

template<typename elemType>
void binaryTree<elemType>::createTree(elemType flag)
{
    linkQueue<Node<elemType> *> que;
    Node<elemType> *tmp;
    elemType x, ldata, rdata;

    std::cin >> x;
    root = new Node<elemType>(root);
    que.enQueue(root);

    while (not que.isEmpty())
    {
        tmp = que.deQueue();
        std::cin >> ldata >> rdata;
        if (ldata not_eq flag) que.enQueue(tmp->left = new Node<elemType>(ldata));
        if (rdata not_eq flag) que.enQueue(tmp->right = new Node<elemType>(rdata));
    }
}

template<typename elemType>
void printTree(const binaryTree<elemType> &t, elemType flag = default_flag)
{
    linkQueue<elemType> q;
    q.enQueue(t.root->data);
    std::cout << std::endl;
    while (not q.isEmpty())
    {
        elemType p, l, r;
        p = q.enQueue();
        l = t.lchild(p, flag);
        r = t.rchild(p, flag);
        std::cout << p << ' ' << l << ' ' << r << std::endl;
        if (l not_eq default_flag) q.enQueue(l);
        if (r not_eq default_flag) q.enQueue(r);
    }
}

template<typename elemType>
Node<elemType> *binaryTree<elemType>::trace(elemType x, Node<elemType> *t) const
{
    if (t == nullptr || (t->left == nullptr && t->right == nullptr))
        return nullptr;
    if ((t->left != nullptr && t->left->data == x) || (t->right != nullptr && t->right->data == x))
        return t;
    if (t->left != nullptr)
    {
        Node<elemType> *temp = trace(x, t->left);
        if (temp != nullptr)
            return temp;
    }
    if (t->right != nullptr)
    {
        Node<elemType> *temp = trace(x, t->right);
        if (temp != nullptr)
            return temp;
    }
    return nullptr;
}

template<typename elemType>
elemType binaryTree<elemType>::parent(elemType x, elemType flag) const
{
    if (root == nullptr || root->data == x)
        return flag;
    Node<elemType> *temp = trace(x, root);
    if (temp == nullptr)
        return flag;
    return temp->data;
}

