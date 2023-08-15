// wtf怎么下面有给hint啊
#include <cstdio>
#include <queue>
const int M = 2005;
const int inf = 10000;
int d[M][M];
int head[M]{}, next[M][M]{}, r[M][M]{};
int n, m;
int flow = 0;

void addEdge(int i, int j, int c)
{
    if (i != j)
    {
        if (d[i][j] == inf && d[j][i] == inf)
            d[i][j] = c, next[i][head[i]] = j, head[i] = j, next[j][head[j]] = i, head[j] = i;
        else
        {
            if (d[i][j] == inf)
                d[i][j] = 0;
            d[i][j] += c;
        }
    }
}

int bfs()
{
    std::queue<int> q;
    q.push(1);
    int prev[M]{}, min[M];
    prev[0] = prev[1] = -1;
    min[0] = min[1] = inf;
    while (!q.empty())
    {
        int x = q.front();
        q.pop();
        for (int i = next[x][0]; i; i = next[x][i])
        {
            int dis = d[x][i] + r[x][i];
            if (dis <= 0 || dis >= inf)
                continue;
            // printf("%d %d dis %d\n", x, i, dis);
            if (prev[i] == 0)
            {
                q.push(i);
                prev[i] = x;
                min[i] = min[x] < dis ? min[x] : dis;
                // printf("min %d=%d\n", i, min[i]);
            }
            if (i == n)
            {
                flow += min[n];
                int y = n;
                // printf("%d \n", min[n]);
                while (prev[y] != -1)
                {
                    // printf("%d ", prev[y]);
                    if (r[prev[y]][y] >= min[n])
                        r[prev[y]][y] -= min[n], d[y][prev[y]] += min[n];
                    else
                        d[prev[y]][y] -= min[n] - r[prev[y]][y], r[y][prev[y]] += min[n] - r[prev[y]][y], r[prev[y]][y] = 0;
                    y = prev[y];
                }
                // printf("\n");
                return 1;
            }
        }
    }
    return 0;
}

int main()
{
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= n; ++j)
            d[i][j] = inf;
    int i, j, c;
    for (int r = 0; r < m; ++r)
        scanf("%d%d%d", &i, &j, &c), addEdge(i, j, c);
    while (bfs())
        ;
    printf("%d\n", flow);
}