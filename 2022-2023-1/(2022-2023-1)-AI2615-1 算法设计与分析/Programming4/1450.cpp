#include <cstdio>
int n;
int b[1005][1005]{};
int to[200000]{}, next[200000]{}, head[200000]{}, cnt = 0;

void addEdge(int u, int v)
{
    // printf("%d %d add\n", u, v);
    to[++cnt] = v;
    next[cnt] = head[u];
    head[u] = cnt;
}
bool vis[205]{};
int viscnt = 0;
int dfs(int s, int p = 0)
{
    // printf("%d\n", s);
    vis[s] = 1, viscnt++;
    int pair = 1;
    for (int i = head[s]; i; i = next[i])
    {
        // printf(" %d %d\n", s, to[i]);

        if (!vis[to[i]] && ((s >= n && to[i] < n) || (to[i] >= n && s < n)))
        {
            // printf("%d %d ", s, to[i]);

            pair = dfs(to[i], s);
            break;
        }
        // if (vis[to[i]] && type[i] + t == 1)
        // {
        //     // printf("%d %d", s, to[i]);
        //     if (to[i] >= n)
        //         b[s][to[i] - n] = 0;
        //     if (s >= n)
        //         b[to[i]][s - n] = 0;
        // }
    }
    if (pair == 1)
    {
        if (s >= n)
            b[p][s - n] = 1;
        else
            b[s][p - n] = 1;
        return 0;
    }
    if (pair == 0)
    {
        return 1;
    }
}
int tot = 0;
int p[1005][1005]{};
int main()
{

    scanf("%d", &n);
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
        {
            scanf("%d", &p[i][j]);
            if (p[i][j])
                addEdge(j + n, i), addEdge(i, j + n);
        }
    for (int i = 1; i <= cnt; ++i)
    {
        // printf("%d\n", to[i]);
        if (vis[to[i]])
            continue;

        if (!dfs(to[i], 1))
        {
            printf("No");
            return 0;
        }
        tot += viscnt;
        viscnt = 0;
    }

    // printf("%d\n", tot);
    int sep = 0;
    if (tot == 2 * n)
    {

        printf("Yes\n");
        for (int i = 0; i < (sep < n ? sep : n); ++i)
        {
            for (int j = 0; j < n; ++j)
                printf("%d ", p[i][j]);
            printf("\n");
        }
        for (int i = sep > 0 ? sep : 0; i < n; ++i)
        {
            for (int j = 0; j < n; ++j)
                printf("%d ", b[i][j]);
            printf("\n");
        }
        return 0;
    }
    else
        printf("Yes\n");
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
            if (!b[i][j] && p[i][j])
            {
                p[i][j] = 0;
                for (int i = 0; i < n; ++i)
                {
                    for (int j = 0; j < n; ++j)
                        printf("%d ", b[i][j]);
                    return 0;
                }
            }
        printf("\n");
    }
}