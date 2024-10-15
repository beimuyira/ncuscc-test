#include <stdio.h>
#include <stdlib.h>

// 冒泡排序函数
void bubble_sort(float arr[], int n) {
    int i, j;
    float temp;
    for (i = 0; i < n-1; i++) {
        for (j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                // 交换 arr[j] 和 arr[j+1]
                temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
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

    // 调用冒泡排序函数对数据进行排序
    bubble_sort(data, n);

    // 输出排序后的数据
    for (i = 0; i < n; i++) {
        printf("%.6f\n", data[i]);
    }

    // 释放动态分配的内存
    free(data);

    return 0;
}
