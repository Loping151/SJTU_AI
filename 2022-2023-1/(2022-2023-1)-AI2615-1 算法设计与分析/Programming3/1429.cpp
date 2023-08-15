#include <cstdio>
#include <algorithm>
const int MM = 1e5 + 5;
int n, m, x;
int s[MM], t[MM];
int index[MM];

inline void read(int &x)
{
    x = 0;
    char ch = getchar();
    while (ch < '0' or ch > '9')
        ch = getchar();
    while (ch >= '0' and ch <= '9')
        x = x * 10 + (ch - 48), ch = getchar();
}

bool cmp(int x, int y)
{
    return t[x] < t[y];
}

int tmp;
int main()
{
    read(m), read(n), read(tmp);
    for (int i = 0; i < n; ++i)
        read(s[i]), read(t[i]), read(tmp);
    for (int i = 0; i < n; ++i)
        index[i] = i;
    std::sort(index, index + n, cmp);
    int time = 0, money = 0;
    for (int i = 0; i < n; ++i)
        if (s[index[i]] > time)
            money += 1, time = t[index[i]];
    printf("%d\n", money);
}