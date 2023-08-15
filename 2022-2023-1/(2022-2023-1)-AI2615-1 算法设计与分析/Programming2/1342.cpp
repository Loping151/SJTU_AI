#include <cstdio>
#include <queue>
#define LL long long int
const LL INF = 9000000000000000;
const int N = 2600;
const int M = 6300 << 1;
int n, m, s, t;
LL dist[N];
LL path[N][N];
int to[M]{}, next[M]{}, head[M]{}, cnt = 0;
LL we[M]{};
template <typename elemType>
class Less
{
public:
    bool operator()(const elemType &left, const elemType &right) const
    {
        return left < right;
    }
};

template <typename elemType>
class Greater
{
public:
    bool operator()(const elemType &left, const elemType &right) const
    {
        return left > right;
    }
};

template <typename elemType, typename compareRule = Less<elemType>>
class priorityQueue
{
private:
    elemType *data;
    int currentLength, maxSize;
    compareRule compare;

    void doubleSpace();

    void update(int current);

    void construct();

public:
    explicit priorityQueue(int size = 100);

    priorityQueue(const elemType input[], int size);

    ~priorityQueue();

    bool empty() const;

    void enQueue(const elemType &element);

    elemType deQueue();

    elemType top() const;

    void clear();
};

template <typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::doubleSpace()
{
    elemType *tempData = data;
    maxSize <<= 1;
    data = new elemType[maxSize + 1];
    for (int i = 0; i <= currentLength; i++)
        data[i] = tempData[i];
    delete[] tempData;
}

template <typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::update(int current)
{
    elemType temp = data[current];
    for (int next; (current << 1) <= currentLength; current = next)
    {
        next = current << 1;
        if (next != currentLength && compare(data[next | 1], data[next]))
            next |= 1;
        if (!compare(data[next], temp))
            break;
        data[current] = data[next];
    }
    data[current] = temp;
}

template <typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::construct()
{
    for (int i = currentLength >> 1; i; i--)
        update(i);
}

template <typename elemType, typename compareRule>
priorityQueue<elemType, compareRule>::priorityQueue(int size) : currentLength(0), maxSize(size)
{
    data = new elemType[size];
}

template <typename elemType, typename compareRule>
priorityQueue<elemType, compareRule>::priorityQueue(const elemType input[], int size) : currentLength(size),
                                                                                        maxSize(size + 10)
{
    data = new elemType[maxSize];
    for (int i = 0; i < size; i++)
        data[i + 1] = input[i];
    construct();
}

template <typename elemType, typename compareRule>
priorityQueue<elemType, compareRule>::~priorityQueue()
{
    delete[] data;
}

template <typename elemType, typename compareRule>
bool priorityQueue<elemType, compareRule>::empty() const
{
    return currentLength == 0;
}

template <typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::enQueue(const elemType &element)
{
    if (currentLength == maxSize - 1)
        doubleSpace();
    int current = ++currentLength;
    while (current > 1 && compare(element, data[current >> 1]))
        data[current] = data[current >> 1], current >>= 1;
    data[current] = element;
}

template <typename elemType, typename compareRule>
elemType priorityQueue<elemType, compareRule>::deQueue()
{
    if (!currentLength)
        printf("Error: Heap is already empty");
    elemType result = data[1];
    data[1] = data[currentLength--];
    update(1);
    return result;
}

template <typename elemType, typename compareRule>
elemType priorityQueue<elemType, compareRule>::top() const
{
    return data[1];
}

template <typename elemType, typename compareRule>
void priorityQueue<elemType, compareRule>::clear()
{
    currentLength = 0;
}

priorityQueue<LL, Less<LL>> q;

void addEdge(int u, int v, int w)
{
    to[++cnt] = v;
    we[cnt] = w;
    next[cnt] = head[u];
    head[u] = cnt;
}

LL convert(LL x, int i = 0)
{
    if (i)
        return 10000 * x + i;
    return x % 10000;
}

template <typename T>
inline void read(T &x)
{
    x = 0;
    char ch = getchar();
    while (ch < '0' || ch > '9')
        ch = getchar();
    while (ch >= '0' && ch <= '9')
        x = x * 10 + (ch - 48), ch = getchar();
}

int main()
{
    int ui, vi, wi;
    read(n), read(m), read(s), read(t);
    for (int i = 1; i <= n; ++i)
    {
        dist[i] = INF;
        for (int j = 1; j <= n; ++j)
            path[i][j] = INF;
    }
    dist[s] = 0;
    for (int i = 0; i < m; ++i)
    {
        read(ui), read(vi), read(wi);
        if (wi < path[ui][vi])
            path[ui][vi] = path[vi][ui] = wi;
    }
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= n; ++j)
            if (path[i][j] != 0 && path[i][j] < INF)
                addEdge(i, j, path[i][j]);
    while (s != t)
    {
        for (int i = head[s]; i; i = next[i])
            if (dist[to[i]] > dist[s] + we[i])
            {
                dist[to[i]] = dist[s] + we[i];
                q.enQueue(convert(dist[to[i]], to[i]));
            }
        s = convert(q.top());
        q.deQueue();
    }
    printf("%lld", dist[t]);
}