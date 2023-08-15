#include <cstdio>
#include <algorithm>
const int M = 3e5 + 5;
int A[M], B[M], Al[M], Bl[M], Ah[M], Bh[M];
int n, cntl = 0, cnth = 0;
int idx[M];
bool cmp(int a, int b)
{
    return Bh[a] < Bh[b];
}
int main()
{
    scanf("%d", &n);
    for (int i = 0; i < n; ++i)
    {
        idx[i] = i;
        scanf("%d%d", &A[i], &B[i]);
        if (A[i] < B[i])
            Al[cntl] = A[i], Bl[cntl++] = B[i];
        if (A[i] > B[i])
            Ah[cnth] = A[i], Bh[cnth++] = B[i];
    }
    std::sort(Al, Al + cntl);
    std::sort(Bl, Bl + cntl);
    std::sort(idx, idx + cnth, cmp);
    int ptrh = 0;

    for (int i = 0; i < n; ++i)
        if (Al[i] < Bl[i])
        {
            if (ptrh == cnth)
            {
                printf("-1\n");
                return 0;
            }
            while (ptrh < cnth)
            {
                if (!(Ah[idx[i]] >= Bl[i] && Al[i] > Bh[idx[i]]))
                    ptrh++;
                else
                    break;
            }
        }

    printf("%d\n", n - cntl);
}