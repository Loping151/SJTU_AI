#include <cstdio>
#include <queue>
using namespace std;
int n, m, s = 1, t, u, v;
int w, ans, dis[500];
int cnt = 1, vis[500], pre[500], head[500], tag[500][500];

struct Edge
{
    int to, net;
    int val;
} edge[500];

inline void add(int u, int v, int w)
{
    edge[++cnt].to = v;
    edge[cnt].val = w;
    edge[cnt].net = head[u];
    head[u] = cnt;
    edge[++cnt].to = u;
    edge[cnt].val = 0;
    edge[cnt].net = head[v];
    head[v] = cnt;
}

inline int bfs()
{
    for (int i = 1; i <= n; i++)
        vis[i] = 0;
    queue<int> q;
    q.push(s);
    vis[s] = 1;
    dis[s] = 500;
    while (!q.empty())
    {
        int x = q.front();
        q.pop();
        for (int i = head[x]; i; i = edge[i].net)
        {
            if (edge[i].val == 0)
                continue;
            int v = edge[i].to;
            if (vis[v] == 1)
                continue;
            dis[v] = min(dis[x], edge[i].val);
            pre[v] = i;
            q.push(v);
            vis[v] = 1;
            if (v == t)
                return 1;
        }
    }
    return 0;
}

inline void update()
{
    int x = t;
    while (x != s)
    {
        int v = pre[x];
        edge[v].val -= dis[t];
        edge[v ^ 1].val += dis[t];
        x = edge[v ^ 1].to;
    }
    ans += dis[t];
}

int main()
{
    scanf("%d%d", &n, &m);
    t = n;
    for (int i = 1; i <= m; i++)
    {
        scanf("%d%d%d", &u, &v, &w);
        if (tag[u][v] == 0)
            add(u, v, w), tag[u][v] = cnt;
        else
            edge[tag[u][v] - 1].val += w;
    }
    while (bfs() != 0)
        update();
    if (ans <= 2000)
        printf("%d", ans);
    return 0;
}
