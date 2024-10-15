#include <stdio.h>
#include <stdlib.h>

// 交换两个浮点数
void swap(float *a, float *b) {
    float temp = *a;
    *a = *b;
    *b = temp;
}

// 堆化函数，将数组调整为最大堆
void heapify(float arr[], int n, int i) {
    int largest = i;       // 初始化最大元素为根节点
    int left = 2 * i + 1;  // 左子节点
    int right = 2 * i + 2; // 右子节点

    // 如果左子节点大于根节点
    if (left < n && arr[left] > arr[largest])
        largest = left;

    // 如果右子节点大于最大节点
    if (right < n && arr[right] > arr[largest])
        largest = right;

    // 如果最大元素不是根节点，交换并递归堆化
    if (largest != i) {
        swap(&arr[i], &arr[largest]);
        heapify(arr, n, largest);
    }
}

// 堆排序函数
void heap_sort(float arr[], int n) {
    // 建堆（最大堆）
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);

    // 一个个从堆中取出元素
    for (int i = n - 1; i >= 0; i--) {
        // 将当前根节点与末尾节点交换
        swap(&arr[0], &arr[i]);

        // 递归堆化，调整堆结构
        heapify(arr, i, 0);
    }
}

int main() {
    int n = 0, i = 0;
    float value;
    float *data = NULL;

    // 动态分配内存空间，初始空间分配为 100 个 float，后续根据需要动态扩展
    int capacity = 100;
    data = (float *)malloc(capacity * sizeof(float));

    if (data == NULL) {
        fprintf(stderr, "内存分配失败\n");
        return 1;
    }

    // 从标准输入读取数据
    while (scanf("%f", &value) != EOF) {
        if (n == capacity) {
            // 如果超过容量，重新分配更大的内存
            capacity *= 2;
            data = (float *)realloc(data, capacity * sizeof(float));
            if (data == NULL) {
                fprintf(stderr, "内存分配失败\n");
                return 1;
            }
        }
        data[n++] = value;
    }

    // 调用堆排序函数对数据进行排序
    heap_sort(data, n);

    // 输出排序后的数据
    for (i = 0; i < n; i++) {
        printf("%.6f\n", data[i]);
    }

    // 释放动态分配的内存
    free(data);

    return 0;
}
