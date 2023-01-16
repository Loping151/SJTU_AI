//
// Created by Kailing Wang on 2022/4/12.
//
#pragma once

#include "set.h"

template<typename keyType, typename DataType>
class dynamicSet
{
public:
    virtual const setElement<keyType, DataType> *find(const keyType &key) const = 0;

    virtual void insert(const setElement<keyType, DataType> &element) = 0;

    virtual void remove(const keyType &key) = 0;

    virtual ~dynamicSet() = default;
};