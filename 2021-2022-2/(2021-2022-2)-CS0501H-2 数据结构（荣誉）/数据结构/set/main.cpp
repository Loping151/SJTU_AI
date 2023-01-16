#include <iostream>
#include "set.h"
#include "staticSet.h"
#include "binarySearchTree.h"
#include "AVLTree.h"

void binarySearchTest()
{
    printf("---------- BinarySearchTree ----------\n");
    setElement<int, std::string> A[] = {
            {10, "aaa"},
            {8,  "bbb"},
            {21, "ccc"},
            {87, "ddd"},
            {56, "eee"},
            {4,  "fff"},
            {11, "ggg"},
            {3,  "hhh"},
            {22, "iiiii"},
            {7,  "jjj"}
    };
    binarySearchTree<int, std::string> T;
    setElement<int, std::string> x;
    const setElement<int, std::string> *p;
    for (auto &i: A)
        T.insert(i);
    if ((p = T.find(56)))
        std::cout << "By key 56 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 56 find nothing\n";
    T.remove(56);
    std::cout << "Now remove element by key 56\n";
    if ((p = T.find(56)))
        std::cout << "By key 56 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 56 find nothing\n";
    if ((p = T.find(21)))
        std::cout << "By key 21 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 21 find nothing\n";
    T.remove(21);
    std::cout << "Now remove element by key 21\n";
    if ((p = T.find(21)))
        std::cout << "By key 21 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 21 find nothing\n";
    if ((p = T.find(30)))
        std::cout << "By key 30 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 30 find nothing\n";
    x = setElement<int, std::string>(30, "xyz");
    T.insert(x);
    std::cout << "Now insert element (30, xyz)\n";
    if ((p = T.find(30)))
        std::cout << "By key 30 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 30 find nothing\n";
    printf("---------- BinarySearchTree ----------\n\n");
}

void AVLTreeTest()
{
    printf("---------- AVLTree ----------\n");
    setElement<int, std::string> A[] = {
            {10, "aaa"},
            {8,  "bbb"},
            {21, "ccc"},
            {87, "ddd"},
            {56, "eee"},
            {4,  "fff"},
            {11, "ggg"},
            {3,  "hhh"},
            {22, "iiiii"},
            {7,  "jjj"}
    };
    AVLTree<int, std::string> T;
    setElement<int, std::string> x;
    const setElement<int, std::string> *p;
    for (auto & i : A)
        T.insert(i);
    if ((p = T.find(56)))
        std::cout << "By key 56 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 56 find nothing\n";
    T.remove(56);
    std::cout << "Now remove element by key 56\n";
    if ((p = T.find(56)))
        std::cout << "By key 56 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 56 find nothing\n";
    if ((p = T.find(21)))
        std::cout << "By key 21 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 21 find nothing\n";
    T.remove(21);
    std::cout << "Now remove element by key 21\n";
    if ((p = T.find(21)))
        std::cout << "By key 21 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 21 find nothing\n";
    if ((p = T.find(30)))
        std::cout << "By key 30 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 30 find nothing\n";
    x = setElement<int, std::string>(30, "xyz");
    T.insert(x);
    std::cout << "Now insert element (30, xyz)\n";
    if ((p = T.find(30)))
        std::cout << "By key 30 find (" << p->key << ", " << p->data << ")\n";
    else
        std::cout << "By key 30 find nothing\n";
    printf("---------- AVLTree ----------\n\n");
}

int main()
{
    printf("---------- StaticSet ----------\n");
    setElement<int, int> S[15];
    for (int i = 1; i <= 10; i++)
    {
        S[i].key = i * 10;
        S[i].data = 1 << i;
    }
    int p = sequentialSearch(S, 10, 51);
    if (!p)
        printf("Key 51 is not found in table\n");
    p = sequentialSearch(S, 10, 60);
    printf("Key 60: key = %d, data = %d\n", S[p].key, S[p].data);
    p = binarySearch(S, 10, 0);
    if (!p)
        printf("Key 0 is not found in table\n");
    p = binarySearch(S, 10, 90);
    printf("Key 90: key = %d, data = %d\n", S[p].key, S[p].data);
    printf("---------- StaticSet ----------\n\n");

    binarySearchTest();
    AVLTreeTest();
}

