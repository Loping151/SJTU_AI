#include <cstdio>
const int N = 2e6 + 5;
int n, m;
int to[N]{}, next[N]{}, head[N]{}, cnt = 0;
int dfn[N ]{}, low[N ], index, instack[N << 1]{}, stack[N << 1], spt = 0;
int scc[N ]{}, scch = 0, sccl[N], sccs, invscc[N << 1];
int root[N];
int res[N];

void addEdge(int u, int v)
{
    to[++cnt] = v;
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

void _tarjan(int x)
{
    dfn[x] = low[x] = ++index;
    instack[x] = 1;
    stack[spt++] = x;
    for (int i = head[x]; i; i = next[i])
    {
        if (not dfn[to[i]])
        {
            _tarjan(to[i]);
            low[x] = low[x] < low[to[i]] ? low[x] : low[to[i]];
        }
        else if (instack[to[i]])
            low[x] = low[x] < dfn[to[i]] ? low[x] : dfn[to[i]];
    }
    if (dfn[x] == low[x])
    {
        sccs = scch;
        while (stack[spt] not_eq x)
        {
            root[stack[--spt]] = x;
            instack[stack[spt]] = 0;
            scc[scch++] = stack[spt];
        }
        sccl[x] = scch - sccs;
    }
}

void tarjan()
{
    for (int i = 1; i <= n << 1; ++i)
    {
        if (dfn[i])
            continue;
        index = 0;
        _tarjan(i);
    }
}

void build(int i, int a, int j, int b)
{
    if (not a and not b)
    {
        addEdge(i + n, j), addEdge(j + n, i);
        return;
    }
    if (not a and b)
    {
        addEdge(i + n, j + n), addEdge(j, i);
        return;
    }
    if (a and not b)
    {
        addEdge(j + n, i + n), addEdge(i, j);
        return;
    }
    if (a and b)
    {
        addEdge(j, i + n), addEdge(i, j + n);
        return;
    }
}

bool scan_yrn()
{
    for (int i = 1; i <= n; ++i)
        if (root[i] == root[i + n])
            return false;
    return true;
}

void confirm(int x, int ch = 1)
{
    if (x > n)
        res[x - n] = 1;
    else
        res[x] = 0;
}

void _scan_sol(int x)
{
    if (res[scc[x] > n ? scc[x] - n : scc[x]] + 1)
        return;
    for (int i = x; i < x + sccl[root[scc[x]]]; ++i)
        confirm(scc[i]);
    for (int i = x; i < x + sccl[root[scc[x]]]; ++i)
        for (int j = head[scc[i]]; j; j = next[j])
            _scan_sol(invscc[to[j]]);
}

void scan_sol()
{
    for (int i = 0; i < n << 1; ++i)
        invscc[scc[i]] = i;
    for (int i = 0; i < n << 1; ++i)
        _scan_sol(i);
}

int ii, a, jj, b;
int main()
{
    read(n), read(m);
    for (int i = 1; i <= n << 1; ++i)
        res[i] = -1;
    for (int i = 0; i < m; ++i)
        read(ii), read(a), read(jj), read(b), build(ii, a, jj, b);
    tarjan();
    if (scan_yrn())
        printf("Yes\n");
    else
    {
        printf("No\n");
        return 0;
    }
    scan_sol();
    for (int i = 1; i <= n; ++i)
        printf("%d ", res[i]);
    return 0;
}
