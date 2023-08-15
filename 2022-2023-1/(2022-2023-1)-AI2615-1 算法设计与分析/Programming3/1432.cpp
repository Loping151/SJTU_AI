#include <cstdio>
#include <algorithm>
const int MM = 1e5 + 5;
int n;
int a[MM], b[MM]{};
int cnt = 1;

int bs(int l, int r, int x)
{
    if (l + 1 >= r)
        return l;
    int m = (l + r) >> 1;
    if (x < b[m])
        return bs(m + 1, r, x);
    else if (x < b[m - 1])
        return m;
    else
        return bs(l, m, x);
}

int insert(int x)
{
    int index;
    b[index = bs(1, cnt, x)] = x;
    // for (int i = 1; i <= cnt; i++)
    //     printf("P%d   ", b[i]);
    return index;
}

int main()
{
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
        scanf("%d", &a[i]);
    b[cnt++] = a[0];
    printf("1 ");
    for (int i = 1; i < n; i++)
    {
        if (a[i] < b[cnt - 1])
            b[cnt++] = a[i], printf("%d ", cnt - 1);
        else
            printf("%d ", insert(a[i]));
    }
}