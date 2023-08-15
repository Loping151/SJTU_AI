#include <cstdio>
#include <queue>
#define LL long long
const LL INF = 10000000000;
const int N = 2600;
const int M = 6300 << 1;
int to[M]{}, next[M]{}, head[M]{}, cnt = 1;
LL we[M]{};
LL dist[N];
int n, m;
std::priority_queue<LL, std::vector<LL>, std::greater<LL>> q;

void addEdge(int u, int v, int w)
{
    to[++cnt] = v;
    we[cnt] = w;
    next[cnt] = head[u];
    head[u] = cnt;
    // printf("Added %d,%d,%lld\n", u, v, w);
}
template <typename T>
inline void read(T &x)
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

LL convert(LL x, int i = 0)
{
    if (i)
        return 10000 * x + (x > 0 ? i : -i);
    return (x > 0 ? x : -x) % 10000;
}

int ui, vi, wi;
int vc = 1;
int s = 1;
int s0 = 0;
bool updated = true;
int stack[N], ps = 0;
bool ins[N]{};
int prev[N];
int main()
{
    read(n), read(m);
    for (int i = 0; i <= m; ++i)
        we[i] = INF << 1;
    for (int i = 1; i <= m; ++i)
        read(ui), read(vi), read(wi), addEdge(ui, vi, wi);

    for (int i = 1; i <= n; ++i) // for every u
    {
        for (int j = 1; j <= n; ++j)
            dist[i] = INF;
        dist[i] = 0;
        for (int k = 1; k <= n; ++k) // for each edge
            for (int h = head[k]; h; h = next[h])
                if (dist[to[h]] > dist[k] + we[h])
                    dist[to[h]] = dist[k] + we[h], prev[to[h]] = k;
        updated = false;
        for (int k = 1; k <= n; ++k) // for each edge
            if (k != i)
                for (int h = head[k]; h; h = next[h])
                    if (dist[to[h]] > dist[k] + we[h])
                        updated = true, s = to[h], dist[to[h]] = dist[k] + we[h], prev[to[h]] = k;
        if (updated)
        {
            while (true)
            {
                stack[ps++] = s;
                ins[s] = true;
                // printf("S is %d\n", s);
                s = prev[s];
                if (ins[s])
                    break;
            }
            stack[ps] = s;
            int pt = 0;
            while (stack[pt] != s)
                ++pt;
            if (s == 0)
            {
                printf("No");
                return 0;
            }
            printf("Yes\n%d\n", ps - pt);
            for (int i = ps; i > pt; --i)
                printf("%d ", stack[i]);
            return 0;
        }
    }
    printf("No");
    return 0;
}