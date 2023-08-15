#include <cstdio>
int n;
double p;

double qpow(double a, int n)
{
    double ans = 1;
    while (n)
    {
        if (n & 1)
            ans *= a;
        a *= a;
        n >>= 1;
    }
    return ans;
}
int main()
{
    scanf("%d", &n);
    scanf("%lf", &p);
    printf("%lf", (2 * n + p * (1 - qpow(p, 2 * n)) / (1 + p)) / (1 + p));
}