#include <cstdio>
// by the way, I'm wangkailing. I guess having multiple accounts is not against the rule.
// I put it here only to watch
// void bubble_sort(int a[], int n)
// {
//     for (int i = 1; i < n; i++)
//     {
//         for (int j = 0; j < n - i; j++)
//         {
//             if (a[j] > a[j + 1])
//             {
//                 swap(a[j], a[j + 1]);
//             }
//         } // after i-th inner iteration, a[n - i] is correct
//     }
// }
#define jian_ding_wei_ni_xu_shu main

inline void read(int &x)
{
    x = 0;
    char ch = getchar();
    while ((ch < '0' || ch > '9') && (ch != '-'))
        ch = getchar();
    while (ch >= '0' && ch <= '9')
        x = x * 10 + (ch - 48), ch = getchar();
}
int n;
int a[1000005], inv[1000005]{}, tmp[1000005];
void merge(int l, int r)
{
    if (l + 1 >= r)
        return;
    int m = (l + r) / 2;
    merge(l, m);
    merge(m, r);
    int cntl = 0, cntr = 0;
    for (int i = l; i < r; ++i)
        if ((a[l + cntl] < a[m + cntr] and l + cntl < m) or m + cntr >= r)
        {
            inv[a[l + cntl]] += cntr;
            tmp[l + cntl + cntr] = a[l + cntl];
            ++cntl;
        }
        else
        {
            inv[a[m + cntr]] += m - l - cntl;
            tmp[l + cntl + cntr] = a[m + cntr];
            ++cntr;
        }
    //干脆merge, obviously faster
    for (int i = l; i < r; ++i)
        a[i] = tmp[i];
}
int jian_ding_wei_ni_xu_shu()
{
    read(n);
    for (int i = 0; i < n; ++i)
        read(a[i]);
    merge(0, n);
    for (int i = 0; i < n; ++i)
        printf("%d ", inv[i + 1]);
}