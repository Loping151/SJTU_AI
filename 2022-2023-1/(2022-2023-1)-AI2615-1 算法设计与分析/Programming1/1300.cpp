#include <algorithm>
#include <cstdio>
#define ull unsigned long long
#define weishenmefangkeshangyuanti main

const int N = 4e7 + 1;
int n, k;
int a[N];
inline void read(int &x)
{
    x = 0;
    char ch = getchar();
    while ((ch < '0' || ch > '9') && (ch != '-'))
        ch = getchar();
    while (ch >= '0' && ch <= '9')
        x = x * 10 + (ch - 48), ch = getchar();
}
void read_input_data()
{
    int m;
    read(n);
    read(k);
    read(m);
    for (int i = 1; i <= m; i++)
    {
        read(a[i]);
    }
    unsigned int z = a[m];
    for (int i = m + 1; i <= n; i++)
    {
        z ^= z << 13;
        z ^= z >> 17;
        z ^= z << 5;
        a[i] = z & 0x7fffffff;
    }
}

int weishenmefangkeshangyuanti()
{
    read_input_data();
    std::nth_element(a + 1, a + k, a + n + 1);
    printf("%d\n", a[k]);
    // will give my own version when I'm free.
}