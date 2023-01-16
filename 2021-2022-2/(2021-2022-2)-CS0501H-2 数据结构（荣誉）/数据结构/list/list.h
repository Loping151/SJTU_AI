//
// Created by loping151 on 2022/2/22.
//

#ifndef LINEAR_LIST_LIST_H
#define LINEAR_LIST_LIST_H

template<typename element_type>
class list
{
public:
    virtual void clear() = 0;

    virtual int length() const = 0;

    virtual void insert(int index, const element_type &x) = 0;

    virtual void remove(int index) = 0;

    virtual int search(const element_type &x) const = 0;

    virtual element_type visit(int index) const = 0;

    virtual void traverse() const = 0;

    virtual ~list() = default;
};

#endif //LINEAR_LIST_LIST_H
