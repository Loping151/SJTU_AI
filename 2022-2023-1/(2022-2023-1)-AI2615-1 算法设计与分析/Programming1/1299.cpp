#include <algorithm>
#include <cmath>
#include <cstdio>
#define ull unsigned long long
int n;
struct point
{
    int x, y;
    point(int x = 0, int y = 0) : x(x), y(y) {}
    point(point const &p) : x(p.x), y(p.y) {}
} p[400005], s[400005];

bool cmpx(point p1, point p2) { return p1.x < p2.x; }
bool cmpy(point p1, point p2) { return p1.y < p2.y; }

ull dis2(point p1, point p2) { return std::pow(p1.x - p2.x, 2) + std::pow(p1.y - p2.y, 2); }

inline void read(int &x)
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

// here I realised there is a python solution given.

ull dc(point set[], int l, int r)
{
    if (l + 1 >= r)
        return 9223372036854775807;
    int m = (l + r) / 2; // what if the data is very edge-focused? Bad
    ull sub1 = dc(set, l, m), sub2 = dc(set, m, r);
    ull ret = sub1 < sub2 ? sub1 : sub2;
    int cnt = 0;
    for (int i = l; i < r; ++i)
        if (std::pow(set[i].x - set[m].x, 2) < ret)
            s[cnt++] = set[i];
    std::sort(s, s + cnt, cmpy);
    for (int i = 0; i < cnt; ++i)
        for (int j = i + 1; j < cnt; ++j)
        {
            if (std::pow(s[i].y - s[j].y, 2) >= ret)
                break;
            ull dis = dis2(s[i], s[j]);
            if (ret > dis)
                ret = dis;
        }
    return ret;
}

int main()
{
    read(n);
    for (int i = 0; i < n; ++i)
    {
        read(p[i].x);
        read(p[i].y);
    }
    std::sort(p, p + n, cmpx);
    printf("%lld\n", dc(p, 0, n));
    return 0;
}