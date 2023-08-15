#include <algorithm>
#include <cstdio>

// attention! This code is already a shit hill
// extreamly unreadable

#define xxy_zhen_nb main
#define f xiang_le_yi_tian

inline void read(int &x)
{
    x = 0;
    char ch = getchar();
    int sign = 0;
    while ((ch < '0' || ch > '9') && (ch != '-'))
        ch = getchar();
    sign = ((ch == '-') && (ch = getchar()));
    while (ch >= '0' && ch <= '9')
        x = x * 10 + (ch - 48), ch = getchar();
    (sign) && (x = -x);
}

int n, s[(1 << 15) + 5], m, ans[20];
int acnt = 0;
bool disd[(1 << 15) + 5]{1, 1};

bool xiang_le_yi_tian(int set[], int len)
{
    if (len == 2)
    {
        if (set[0] == 0 or set[1] == 0)
        {
            ans[acnt++] = set[0] + set[1];
            return true;
        }
        --acnt;
        return false;
    }
    for (int i = 2; i < len; ++i)
        disd[i] = false;
    int min = set[0], min2 = set[1];
    int abs_elem = min2 - min;
    int *p1 = new int[len / 2], *p2 = new int[len / 2];
    int ptl = 2, ptr = 3;
    int cntl = 1, cntr = 1;
    p1[0] = min, p2[0] = min2;
    while (ptl < len)
    {
        if (ptr > len)
        {
            --acnt;
            return false;
        }
        if (set[ptl] == set[ptr] - abs_elem)
        {
            p1[cntl++] = set[ptl];
            p2[cntr++] = set[ptr];
            disd[ptr] = true;
            while (disd[++ptl])
                ;
        }
        ++ptr;
        if (ptl == ptr)
            ptr++;
    }
    if (not(cntl == len / 2))
    {
        --acnt;
        return false;
    }
    ans[acnt++] = abs_elem;
    bool re1 = f(p1, len / 2);
    bool re2 = 0;
    if (not re1)
    {
        ans[acnt++] = -abs_elem;
        re2 = f(p2, len / 2);
    }
    delete[] p1;
    delete[] p2;
    if (not re1 and not re2)
        --acnt;
    return re1 or re2;
}

int xxy_zhen_nb()
{
    read(n);
    m = (1 << n);
    s[0] = 0; // add empty set
    for (int i = 1; i < m; ++i)
        read(s[i]);
    std::sort(s, s + m);
    if (not f(s, m))
        printf("NO\n");
    else
    {
        printf("YES\n");
        for (int i = 0; i < acnt; ++i)
            printf("%d ", ans[i]);
    }
}