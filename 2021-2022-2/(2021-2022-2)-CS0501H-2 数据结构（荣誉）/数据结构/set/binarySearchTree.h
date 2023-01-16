//
// Created by Kailing Wang on 2022/4/12.
//

#pragma once

#include"dynamicSet.h"

template<typename keyType, typename dataType>
class binarySearchTree : public dynamicSet<keyType, dataType>
{
private:
    struct treeNode
    {
        setElement<keyType, dataType> data;
        treeNode *left, *right;

        treeNode() : data(), left(nullptr), right(nullptr) {}

        explicit treeNode(const setElement<keyType, dataType> &_data, treeNode *_left = nullptr,
                          treeNode *_right = nullptr)
                : data(_data), left(_left), right(_right) {}
    };

    treeNode *root;

    const setElement<keyType, dataType> *find(treeNode *current, const keyType &key) const;

    void insert(treeNode *&current, const setElement<keyType, dataType> &element);

    void remove(treeNode *&current, const keyType &key);

    void clear(treeNode *current);

public:
    binarySearchTree();

    ~binarySearchTree();

    const setElement<keyType, dataType> *find(const keyType &key) const;

    void insert(const setElement<keyType, dataType> &element);

    void remove(const keyType &key);

    void clear();
};

template<typename keyType, typename dataType>
const setElement<keyType, dataType> *
binarySearchTree<keyType, dataType>::find(treeNode *current, const keyType &key) const
{
    if (not current)
        return nullptr;
    if (key == (current->data).key)
        return &(current->data);
    if (key < (current->data).key)
        return find(current->left, key);
    else
        return find(current->right, key);
}

template<typename keyType, typename dataType>
void binarySearchTree<keyType, dataType>::insert(treeNode *&current, const setElement<keyType, dataType> &element)
{
    if (not current)
        current = new treeNode(element);
    else if (element.key < (current->data).key)
        insert(current->left, element);
    else if (element.key > (current->data).key)
        insert(current->right, element);
}

template<typename keyType, typename dataType>
void binarySearchTree<keyType, dataType>::remove(treeNode *&current, const keyType &key)
{
    if (not current)
        return;
    if (key < (current->data).key)
        remove(current->left, key);
    else if (key > (current->data).key)
        remove(current->right, key);
    else if (current->left && current->right)
    {
        treeNode *tmp = current->right;
        while (tmp->left)
            tmp = tmp->left;
        current->data = tmp->data;
        remove(current->right, (current->data).key);
    }
    else
    {
        treeNode *tmp = current;
        if (current->left)
            current = current->left;
        else
            current = current->right;
        delete tmp;
    }
}

template<typename keyType, typename dataType>
void binarySearchTree<keyType, dataType>::clear(treeNode *current)
{
    if (not current)
        return;
    clear(current->left);
    clear(current->right);
    delete current;
}

template<typename keyType, typename dataType>
binarySearchTree<keyType, dataType>::binarySearchTree()
{
    root = nullptr;
}

template<typename keyType, typename dataType>
binarySearchTree<keyType, dataType>::~binarySearchTree()
{
    clear(root);
    root = nullptr;
}

template<typename keyType, typename dataType>
const setElement<keyType, dataType> *binarySearchTree<keyType, dataType>::find(const keyType &key) const
{
    return find(root, key);
}

template<typename keyType, typename dataType>
void binarySearchTree<keyType, dataType>::insert(const setElement<keyType, dataType> &element)
{
    insert(root, element);
}

template<typename keyType, typename dataType>
void binarySearchTree<keyType, dataType>::remove(const keyType &key)
{
    remove(root, key);
}

template<typename keyType, typename dataType>
void binarySearchTree<keyType, dataType>::clear()
{
    clear(root);
    root = nullptr;
}