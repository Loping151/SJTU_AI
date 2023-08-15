#include <iostream>
#include <queue>
#define LL long long
#define INF 9223372036854775807
const int N = 2600;
const int M = 6300 << 1;
int n, m, s, t;
int to[M]{}, next[M]{}, head[M]{}, we[M]{}, cnt = 0;
LL dist[N];
std::priority_queue<LL, std::vector<LL>, std::greater<LL>> q;

LL convert(LL x, int i = 0)
{
    if (i)
        return 100000 * x + i;
    return x % 100000;
}
void addEdge(int u, int v, int w)
{
    to[++cnt] = v;
    we[cnt] = w;
    next[cnt] = head[u];
    head[u] = cnt;
}

inline void read(int &x)
{
    x = 0;
    char ch = getchar();
    while (ch < '0' or ch > '9')
        ch = getchar();
    while (ch >= '0' and ch <= '9')
        x = x * 10 + (ch - 48), ch = getchar();
}

int main()
{
    q.push(9999999990001);
    q.push(99999999900001);
    q.push(99999999900002);
    q.push(99999999900003);
    std::cout << q.top() << std::endl;
}