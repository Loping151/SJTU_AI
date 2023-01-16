//
// Created by Kailing Wang on 2022/4/12.
//

#pragma once

template<typename keyType, typename DataType>
class setElement
{
public:
    keyType key;
    DataType data;

    setElement() : key(), data() {}

    setElement(keyType _key, DataType _data) : key(_key), data(_data) {}

    setElement &operator=(const setElement &another)
    {
        key = another.key;
        data = another.data;
        return *this;
    }
};
