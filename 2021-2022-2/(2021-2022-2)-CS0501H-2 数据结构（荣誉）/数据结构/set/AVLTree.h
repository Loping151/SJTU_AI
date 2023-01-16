#pragma once

#include "dynamicSet.h"

template<typename elemType>
elemType max(const elemType &x, const elemType &y)
{
    return (x > y) ? x : y;
}

template<typename keyType, typename dataType>
class AVLTree : public dynamicSet<keyType, dataType>
{
private:
    struct AVLNode
    {
        setElement<keyType, dataType> data;
        AVLNode *left, *right;
        int height;

        AVLNode() : data(), left(nullptr), right(nullptr), height(1) {}

        explicit AVLNode(const setElement<keyType, dataType> &elem, AVLNode *l = nullptr, AVLNode *r = nullptr, int h = 1) : data(elem), left(l), right(r), height(h) {}
    };

    AVLNode *root;

    void RR(AVLNode *&current);

    void LL(AVLNode *&current);

    void LR(AVLNode *&current);

    void RL(AVLNode *&current);

    int height(AVLNode *current) const;

    bool adjust(AVLNode *&current, bool isRight);

    void insert(AVLNode *&current, const setElement<keyType, dataType> &element);

    bool remove(AVLNode *&current, const keyType &key);

    void clear(AVLNode *current);

public:
    AVLTree();

    ~AVLTree();

    const setElement<keyType, dataType> *find(const keyType &key) const;

    void insert(const setElement<keyType, dataType> &element);

    void remove(const keyType &key);

    void clear();
};

template<typename keyType, typename dataType>
int AVLTree<keyType, dataType>::height(AVLNode *current) const
{
    if (current == nullptr)
        return 0;
    else
        return current->height;
}

template<typename keyType, typename dataType>
bool AVLTree<keyType, dataType>::adjust(AVLNode *&current, bool isRight)
{
    if (isRight)
    {
        if (height(current->left) - height(current->right) == 1)
            return true;
        if (height(current->left) == height(current->right))
        {
            (current->height)--;
            return false;
        }
        if (height(current->left->right) > height(current->left->left))
        {
            LR(current);
            return false;
        }
        RR(current);
        return height(current->left) != height(current->right);
    }
    else
    {
        if (height(current->right) - height(current->left) == 1)
            return true;
        if (height(current->right) == height(current->left))
        {
            (current->height)--;
            return false;
        }
        if (height(current->right->left) > height(current->right->right))
        {
            RL(current);
            return false;
        }
        LL(current);
        return height(current->right) != height(current->left);
    }
}

template<typename keyType, typename dataType>
void AVLTree<keyType, dataType>::insert(AVLNode *&current, const setElement<keyType, dataType> &element)
{
    if (current == nullptr)
        current = new AVLNode(element);
    else if (element.key < (current->data).key)
    {
        insert(current->left, element);
        if (height(current->left) - height(current->right) == 2)
        {
            if (element.key < (current->left->data).key)
                RR(current);
            else
                LR(current);
        }
    }
    else if (element.key > (current->data).key)
    {
        insert(current->right, element);
        if (height(current->right) - height(current->left) == 2)
        {
            if (element.key > (current->right->data).key)
                LL(current);
            else
                RL(current);
        }
    }
    current->height = max(height(current->left), height(current->right)) + 1;
}

template<typename keyType, typename dataType>
bool AVLTree<keyType, dataType>::remove(AVLNode *&current, const keyType &key)
{
    if (current == nullptr)
        return true;
    if (key == (current->data).key)
    {
        if (current->left == nullptr || current->right == nullptr)
        {
            AVLNode *tmp = current;
            if (current->left != nullptr)
                current = current->left;
            else
                current = current->right;
            delete tmp;
            return false;
        }
        else
        {
            AVLNode *tmp = current->right;
            while (tmp->left != nullptr)
                tmp = tmp->left;
            current->data = tmp->data;
            if (remove(current->right, (tmp->data).key))
                return true;
            return adjust(current, 1);
        }
    }
    if (key < (current->data).key)
    {
        if (remove(current->left, key))
            return true;
        return adjust(current, 0);
    }
    else
    {
        if (remove(current->right, key))
            return true;
        return adjust(current, 1);
    }
}

template<typename keyType, typename dataType>
void AVLTree<keyType, dataType>::clear(AVLNode *current)
{
    if (current == nullptr)
        return;
    clear(current->left);
    clear(current->right);
    delete current;
}

template<typename keyType, typename dataType>
void AVLTree<keyType, dataType>::RR(AVLNode *&current)
{
    AVLNode *child = current->left;
    current->left = child->right;
    child->right = current;
    current->height = max(height(current->left), height(current->right)) + 1;
    child->height = max(height(child->left), height(child->right)) + 1;
    current = child;
}

template<typename keyType, typename dataType>
void AVLTree<keyType, dataType>::LL(AVLNode *&current)
{
    AVLNode *child = current->right;
    current->right = child->left;
    child->left = current;
    current->height = max(height(current->left), height(current->right)) + 1;
    child->height = max(height(child->left), height(child->right)) + 1;
    current = child;
}

template<typename keyType, typename dataType>
void AVLTree<keyType, dataType>::LR(AVLNode *&current)
{
    LL(current->left);
    RR(current);
}

template<typename keyType, typename dataType>
void AVLTree<keyType, dataType>::RL(AVLNode *&current)
{
    RR(current->right);
    LL(current);
}

template<typename keyType, typename dataType>
const setElement<keyType, dataType> *AVLTree<keyType, dataType>::find(const keyType &key) const
{
    AVLNode *current = root;
    while (current != nullptr && (current->data).key != key)
    {
        if ((current->data).key > key)
            current = current->left;
        else
            current = current->right;
    }
    if (current == nullptr)
        return nullptr;
    return &(current->data);
}

template<typename keyType, typename dataType>
void AVLTree<keyType, dataType>::insert(const setElement<keyType, dataType> &element)
{
    insert(root, element);
}

template<typename keyType, typename dataType>
void AVLTree<keyType, dataType>::remove(const keyType &key)
{
    remove(root, key);
}

template<typename keyType, typename dataType>
AVLTree<keyType, dataType>::AVLTree()
{
    root = nullptr;
}

template<typename keyType, typename dataType>
AVLTree<keyType, dataType>::~AVLTree()
{
    clear(root);
    root = nullptr;
}

template<typename keyType, typename dataType>
void AVLTree<keyType, dataType>::clear()
{
    clear(root);
    root = nullptr;
}