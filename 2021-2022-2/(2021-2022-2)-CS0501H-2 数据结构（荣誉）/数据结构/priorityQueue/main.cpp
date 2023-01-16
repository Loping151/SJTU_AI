#include <iostream>

#include "priorityQueue.h"


int main()
{
    printf("---------- PriorityQueue ----------\n");
    priorityQueue<int> heap;
    int array[15] = {7, 4, 1, 6, 5, 9, 3, 0, 8, 2};
    for (int i = 0; i < 10; i++)
        heap.enQueue(array[i]);
    for (int i = 0; i < 10; i++)
        printf("%d ", heap.deQueue());
    printf("\n");
    heap.clear();
    for (int i = 0; i < 10; i++)
        array[i] = i;
    priorityQueue<int, Greater<int>> queue(array, 10);
    for (int i = 1; i <= 5; i++)
        queue.enQueue(100 + i);
    for (int i = 0; i < 15; i++)
    {
        int x = queue.top();
        queue.deQueue();
        printf("%d ", x);
    }
    printf("\n");
    heap.clear();
    if (heap.empty())
        printf("Now heap is already empty!\n");
    printf("---------- PriorityQueue ----------\n\n");
}
