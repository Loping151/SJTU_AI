#include <cstdio>
#include <queue>
#define LL long long
std::priority_queue<LL, std::vector<LL>, std::greater<LL>> q;
int n, w, p;
LL money;

template <typename T>
inline T read(T &x)
{
    x = 0;
    char ch = getchar();
    while (ch < '0' or ch > '9')
        ch = getchar();
    while (ch >= '0' and ch <= '9')
        x = x * 10 + (ch - 48), ch = getchar();
    return x;
}

LL tmp;

int main()
{
    read(n), read(w), read(p);
    for (int i = 0; i < n; ++i)
        q.push((read(tmp)));
    LL sum = 0;
    LL d1, d2;
    while (q.size() > 1)
    {
        d1 = q.top(), q.pop();
        d2 = q.top(), q.pop();
        q.push(d1 + d2);
        sum += d1 + d2;
    }
    LL money = sum * p / 100;
    if (sum * p - 100 * money)
        money++;
    printf("%lld", money);
}