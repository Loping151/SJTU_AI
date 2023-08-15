#include <cstdio>
#include <queue>
std::queue<int> q;
const int MAX = 2e5 + 10;
int head[MAX << 1]{}, next[MAX << 1]{}, to[MAX << 1]{}, cnt = 0;
int cyc[MAX]{}, far[MAX];
int vis[MAX]{};

void add(int u, int v)
{
    if (u == v)
        cyc[u] = 1;
    else
    {
        to[++cnt] = v;
        next[cnt] = head[u];
        head[u] = cnt;
        to[++cnt] = u;
        next[cnt] = head[v];
        head[v] = cnt;
    }
}
int n, m, s, t, k;
int odd = 0, even = 0;
void bfs()
{
    while (!q.empty())
    {
        int x = q.front();
        // printf("%d", x);
        q.pop();
        vis[x] = 1;
        for (int i = head[x]; i; i = next[i])
        {
            if (!vis[to[i]])
            {

                far[to[i]] = far[x] + 1;
                cyc[to[i]] += cyc[x];
                q.push(to[i]);
            }
            if (to[i] == t && far[to[i]] + 1 <= k)
                if (far[x] % 2)
                    even = 1;
                else
                    odd = 1;
        }
    }
}
int main()
{
    int u, v;
    scanf("%d%d%d%d%d", &n, &m, &s, &t, &k);
    for (int i = 0; i < m; ++i)
        scanf("%d%d", &u, &v), add(u, v);
    int dis = 0;
    q.push(s);
    far[s] = 0;
    bfs();
    if (odd && even || cyc[t] && far[t] <= k)
        printf("Yes");
    else if (odd && k % 2)
        printf("Yes");
    else if (even && k % 2 == 0)
        printf("Yes");
    else
        printf("No");
}