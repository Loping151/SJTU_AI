//
// Created by loping151 on 2022/2/22.
//

#ifndef LINEAR_LIST_SEQ_LIST_H
#define LINEAR_LIST_SEQ_LIST_H

#include "list.h"

template<typename element_type>
class seq_list : public list<element_type>
{
private:
    element_type *data;
    int current_length;
    int max_size;

    void double_space();

public:
    explicit seq_list(int initial_length = 10);

    ~seq_list();

    void clear();

    int length() const;

    void insert(int index, const element_type &x);

    void remove(int index);

    int search(const element_type &x) const;

    element_type visit(int index) const;

    void traverse() const;
};


#endif //LINEAR_LIST_SEQ_LIST_H
