#include <cstdio>
#include <iostream>
using namespace std;

namespace LIST
{

    struct NODE
    {
        // TODO
        int data{};
        NODE *next = nullptr;
        NODE() : next(nullptr){};
        explicit NODE(int data, NODE *next = nullptr) : data(data), next(next) {}
    };

    NODE *head = nullptr;
    int len = 0;

    void init()
    {
        // TODO
        head = new NODE;
        head->next = nullptr;
    }
    NODE *move(int i)
    {
        // TODO
        NODE *p = head;

        while (i-- >= 0)
            p = p->next;
        return p;
    }
    void insert(int i, int x)
    {
        // TODO
        NODE *pos;
        if (i == 0)
            pos = head;
        else
            pos = move(i - 1);
        pos->next = new NODE(x, pos->next);
        ++len;
    }
    void remove(int i)
    {
        // TODO
        NODE *pos, *del;

        if (i == 0)
            pos = head;
        else
            pos = move(i - 1);
        del = pos->next;
        pos->next = del->next;
        delete del;
        --len;
    }
    void remove_insert(int i)
    {
        // TODO
        NODE *pos, *del;

        if (i == 0)
            pos = head;
        else
            pos = move(i - 1);
        del = pos->next;
        pos->next = del->next;
        pos = move(len - 1);
        pos->next = new NODE(del->data);
        delete del;
    }
    void get_length()
    {
        // TODO
        cout << len << '\n';
    }
    void query(int i)
    {
        // TODO
        if (i < 0 or i >= len)
            cout << -1 << '\n';
        else
        {
            NODE *p = move(i);
            cout << p->data << '\n';
        }
    }
    void get_max()
    {
        // TODO
        NODE *p = head->next;
        if (p == nullptr)
        {
            cout << -1 << '\n';
            return;
        }
        else
        {
            int max = p->data;
            while (p != nullptr)
            {
                if (p->data > max)
                    max = p->data;
                p = p->next;
            }
            cout << max << '\n';
        }
    }
    void clear()
    {
        // TODO
        NODE *p = head, *q = nullptr;
        if (p->next == nullptr)
            return;
        else
        {
            while (p->next != nullptr)
            {
                q = p->next;
                delete p;
                p = q;
            }
        }
    }
}
int n;
int main()
{
    cin >> n;
    int op, x, p;
    LIST::init();
    for (int _ = 0; _ < n; ++_)
    {
        cin >> op;
        switch (op)
        {
            case 0:
                LIST::get_length();
                break;
            case 1:
                cin >> p >> x;
                LIST::insert(p, x);
                break;
            case 2:
                cin >> p;
                LIST::query(p);
                break;
            case 3:
                cin >> p;
                LIST::remove(p);
                break;
            case 4:
                cin >> p;
                LIST::remove_insert(p);
                break;
            case 5:
                LIST::get_max();
                break;
        }
    }
    LIST::clear();
    return 0;
}