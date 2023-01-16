#ifndef BINOMIAL_QUEUE_H
#define BINOMIAL_QUEUE_H

using namespace std;

template<typename Comparable>
class binomialQueue
{
public:
    binomialQueue() : theTrees(DEFAULT_TREES)
    {
        for (auto &root: theTrees)
            root = nullptr;
        currentSize = 0;
    }

    binomialQueue(const Comparable &item) : theTrees(1), currentSize{1}
    {
        theTrees[0] = new BinomialNode{item, nullptr, nullptr};
    }

    binomialQueue(const binomialQueue &rhs)
            : theTrees(rhs.theTrees.size()), currentSize{rhs.currentSize}
    {
        for (int i = 0; i < rhs.theTrees.size(); ++i)
            theTrees[i] = clone(rhs.theTrees[i]);
    }

    binomialQueue(binomialQueue &&rhs)
            : theTrees{std::move(rhs.theTrees)}, currentSize{rhs.currentSize} {}

    ~binomialQueue()
    {
        makeEmpty();
    }

    binomialQueue &operator=(const binomialQueue &rhs)
    {
        binomialQueue copy = rhs;
        std::swap(*this, copy);
        return *this;
    }

    binomialQueue &operator=(binomialQueue &&rhs)
    {
        std::swap(currentSize, rhs.currentSize);
        std::swap(theTrees, rhs.theTrees);
        return *this;
    }

    bool isEmpty() const
    {
        return currentSize == 0;
    }

    const Comparable &findMin() const
    {
        if (isEmpty())
            throw UnderflowException{};
        return theTrees[findMinIndex()]->element;
    }

    void insert(const Comparable &x)
    {
        binomialQueue oneItem{x};
        merge(oneItem);
    }

    void insert(Comparable &&x)
    {
        binomialQueue oneItem{std::move(x)};
        merge(oneItem);
    }

    void deleteMin()
    {
        Comparable x;
        deleteMin(x);
    }

    void deleteMin(Comparable &minItem)
    {
        if (isEmpty())
            throw UnderflowException{};
        int minIndex = findMinIndex();
        minIndex = theTrees[minIndex]->element;
        BinomialNode *oldRoot = theTrees[minIndex];
        BinomialNode *deletedTree = oldRoot->leftchild;
        delete oldRoot;

        binomialQueue deletedQueue;
        deletedQueue.theTrees.resize(minIndex + 1);
        deletedQueue.currentSize = (1 << minIndex) - 1;
        for (int j = minIndex - 1; j >= 0; --j)
        {
            deletedQueue.theTrees[j] = deletedTree;
            deletedTree = deletedTree->nextSibling;
            deletedQueue.theTrees[j]->nextSibling = nullptr;
        }

        theTrees[minIndex] = nullptr;
        currentSize -= deletedQueue.currentSize + 1;

        merge(deletedQueue);
    }

    void makeEmpty()
    {
        currentSize = 0;
        for (auto &root: theTrees)
            makeEmpty(root);
    }

    void merge(binomialQueue &rhs)
    {
        if (this == &rhs)
            return;

        currentSize += rhs.currentSize;

        if (currentSize > capacity())
        {
            int oldNumTrees = theTrees.size();
            int newNumTrees = max(theTrees.size(), rhs.theTrees.size()) + 1;
            theTrees.resize(newNumTrees);
            for (int i = oldNumTrees; i < newNumTrees; ++i)
                theTrees[i] = nullptr;
        }

        BinomialNode *carry = nullptr;
        for (int i = 0, j = 1; j <= currentSize; ++i, j *= 2)
        {
            BinomialNode *t1 = theTrees[i];
            BinomialNode *t2 = i < rhs.theTrees.size() ? rhs.theTrees[i] : nullptr;
            int whichCase = t1 == nullptr ? 0 : 1;
            whichCase += t2 == nullptr ? 0 : 2;
            whichCase += carry == nullptr ? 0 : 4;

            switch (whichCase)
            {
                case 0: /* No trees */
                case 1: /* Only this */
                    break;
                case 2:
                    theTrees[i] = t2; /* Only rhs */
                    rhs.theTrees[i] = nullptr;
                    break;
                case 4: /* Only carry */
                    theTrees[i] = carry;
                    carry = nullptr;
                    break;
                case 3: /* this and rhs */
                    carry = combineTrees(t1, t2);
                    theTrees[i] = rhs.theTrees[i] = nullptr;
                    break;
                case 5: /* this and carry */
                    carry = combineTrees(t1, carry);
                    theTrees[i] = nullptr;
                    break;
                case 6: /* rhs and carry */
                    carry = combineTrees(t2, carry);
                    rhs.theTrees[i] = nullptr;
                    break;
                case 7: /* All three */
                    theTrees[i] = carry;
                    carry = combineTrees(t1, t2);
                    rhs.theTrees[i] = nullptr;
                    break;
            }
        }
        for (auto &root: rhs.theTrees)
            root = nullptr;
        rhs.currentSize = 0;
    }

private:
    struct BinomialNode
    {
        Comparable element;
        BinomialNode *leftchild;
        BinomialNode *nextSibling;

        BinomialNode(const Comparable &e, BinomialNode *lt, BinomialNode *rt)
                : element{e}, leftchild{lt}, nextSibling{rt} {}

        BinomialNode(Comparable &&e, BinomialNode *lt, BinomialNode *rt)
                : element{std::move(e)}, leftchild{lt}, nextSibling{rt} {}
    };

    const static int DEFAULT_TREES = 1;

    vector<BinomialNode *> theTrees;
    int currentSize;

    int findMinIndex() const
    {
        int i;
        int minIndex;
        for (i = 0; theTrees[i] == nullptr; ++i);
        for (minIndex = i; i < theTrees.size(); ++i)
            if (theTrees[i] != nullptr && theTrees[i]->element < theTrees[minIndex]->element)
                minIndex = i;

        return minIndex;
    }

    int capacity() const
    {
        return (1 << theTrees.size()) - 1;
    }

    BinomialNode *combineTrees(BinomialNode *t1, BinomialNode *t2)
    {
        if (t2->element < t1->element)
            return combineTrees(t2, t1);
        t2->nextSibling = t1->leftchild;
        t1->leftchild = t2;
        return t1;
    }

    void makeEmpty(BinomialNode *&t)
    {
        if (t != nullptr)
        {
            makeEmpty(t->leftchild);
            makeEmpty(t->nextSibling);
            delete t;
            t = nullptr;
        }
    }

    BinomialNode *clone(BinomialNode *t) const
    {
        if (t == nullptr)
            return nullptr;
        else
            return new BinomialNode{t->element, clone(t->leftchild), clone(t->nextSibling)};
    }
};

#endif
