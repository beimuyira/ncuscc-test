    // 依次提取最小值
    for (int i = 0; i < n; i++) {
        FibonacciNode* min = remove_min(heap);
        if (min != NULL) {
            arr[i] = min->key;
            free(min);
        }
    }


    // 释放堆内存
    free(heap);
}


int main() {
    int n = 0, i = 0;
    float value;
    float *data = NULL;


    // 动态分配内存空间，初始分配为 100 个 float
    int capacity = 100;
    data = (float *)malloc(capacity * sizeof(float));


    if (data == NULL) {
        fprintf(stderr, "内存分配失败\n");
        return 1;
    }


    // 从标准输入读取数据
    while (scanf("%f", &value) != EOF) {
        if (n == capacity) {
            // 超过容量时重新分配内存
            capacity *= 2;
            data = (float *)realloc(data, capacity * sizeof(float));
            if (data == NULL) {
                fprintf(stderr, "内存分配失败\n");
                return 1;
            }
        }
        data[n++] = value;
    }


    // 使用斐波那契堆排序
    fibonacci_heap_sort(data, n);


    // 输出排序结果
    for (i = 0; i < n; i++) {
        printf("%.6f\n", data[i]);
    }


    // 释放内存
    free(data);


    return 0;
}
