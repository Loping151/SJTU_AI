#include <cstdio>
#include <queue>
#define LL long long
std::priority_queue<int, std::vector<int>, std::greater<int>> q;

LL money = 0;
int n;

inline int read(int &x)
{
    x = 0;
    char ch = getchar();
    while (ch < '0' or ch > '9')
        ch = getchar();
    while (ch >= '0' and ch <= '9')
        x = x * 10 + (ch - 48), ch = getchar();
    return x;
}

int tmp;
int main()
{
    read(n);
    for (int i = 0; i < n; ++i)
    {
        q.push(read(tmp));
        if (tmp > q.top())
            money += tmp - q.top(), q.pop(), q.push(tmp);
    }
    printf("%lld", money);
}