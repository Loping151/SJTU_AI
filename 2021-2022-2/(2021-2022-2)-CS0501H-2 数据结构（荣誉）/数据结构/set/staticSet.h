//
// Created by Kailing Wang on 2022/4/12.
//

#pragma once

#include "set.h"

template<typename keyType, typename dataType>
int sequentialSearch(setElement<keyType, dataType> table[], int size, const keyType &key)
{
    int i;
    table[0].key = key;
    for (i = size; table[i].key != key; i--);
    return i;
}

template<typename keyType, typename dataType>
int binarySearch(setElement<keyType, dataType> table[], int size, const keyType &key)
{
    int l = 1, r = size, h;
    while (l <= r)
    {
        h = (l + r) >> 1;
        if (table[h].key == key)
            return h;
        if (table[h].key > key)
            r = h - 1;
        else
            l = h + 1;
    }
    return 0;
}