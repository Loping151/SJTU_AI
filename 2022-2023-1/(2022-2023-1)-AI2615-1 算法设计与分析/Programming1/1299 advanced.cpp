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
} p[400005], s[400005], p2[400005];

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

ull dc(int x1, int x2, int y1, int y2)
{
    if (x1 + 1 >= x2 or y1 + 1 >= y2)
        return 9223372036854775807;
    int mx = (x1 + x2) / 2;
    int my = (y1 + y2) / 2;
    ull sub1 = dc(x1, mx, y1, my), sub2 = dc(mx, x2, y1, my);
    ull sub3 = dc(x1, mx, my, y2), sub4 = dc(mx, x2, my, y2);
    ull ret = std::min(std::min(sub1, sub2), std::min(sub3, sub4));
    int cnt = 0;
    for (int i = x1; i < x2; ++i)
        if (std::pow(p[i].x - p[mx].x, 2) < ret)
            s[cnt++] = p[i];
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
    cnt = 0;
    for (int i = y1; i < y2; ++i)
        if (std::pow(p2[i].y - p2[my].y, 2) < ret)
            s[cnt++] = p2[i];
    std::sort(s, s + cnt, cmpx);
    for (int i = 0; i < cnt; ++i)
        for (int j = i + 1; j < cnt; ++j)
        {
            if (std::pow(s[i].x - s[j].x, 2) >= ret)
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
        p2[i] = p[i];
    }
    std::sort(p, p + n, cmpx);
    std::sort(p2, p2 + n, cmpy);
    printf("%lld\n", dc(0, n, 0, n));
    return 0;
}