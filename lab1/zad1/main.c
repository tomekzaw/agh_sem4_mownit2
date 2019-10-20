#include <stdlib.h>
#include <stdio.h>
#include <time.h>

typedef struct errors {
    float absolute, relative;
} errors;

errors calc_errors(float x, float x0) {
    errors err;
    err.absolute = x - x0;
    err.relative = err.absolute / x0;
    return err;
}

float sum_simple(float t[], int n) {
    float sum = 0.0f;
    for (int i = 0; i < n; i++) {
        sum += t[i];
    }
    printf("\n");
    return sum;
}

float sum_recursive_lr(float t[], int l, int r) {
    if (l > r) {
        return 0.0f;
    }
    if (l == r) {
        return t[l];
    }
    return sum_recursive_lr(t, l, l+(r-l)/2) + sum_recursive_lr(t, l+(r-l)/2+1, r);
}

float sum_recursive(float t[], int n) {
    return sum_recursive_lr(t, 0, n-1);
}

float sum_kahana(float tab[], int n) {
    float sum = 0.0f;
    float err = 0.0f;
    for (int i = 0; i < n; ++i) {
        float y = tab[i] - err;
        float temp = sum + y;
        err = (temp - sum) - y;
        sum = temp;
    }
    return sum;
}

int main() {
    const int N = 1e7;
    float x = 0.53125f;

    float* t = (float*) malloc(sizeof(float) * N);
    if (t == NULL) {
        fprintf(stderr, "Cannot allocate array");
        return 1;
    }

    for (int i = 0; i < N; i++) {
        t[i] = x;
    }

    clock_t c = clock();
    float sum = sum_simple(t, N);
    c = clock() - c;
    double seconds = ((double) c) / CLOCKS_PER_SEC;
    errors err = calc_errors(x*N, sum);

    printf("simple sum: %f\n", sum);
    printf("absolute error: %f\n", err.absolute);
    printf("relative error: %f = %f%%\n", err.relative, err.relative * 100);
    printf("%f s\n\n", seconds);

    c = clock();
    sum = sum_recursive(t, N);
    c = clock() - c;
    seconds = ((double) c) / CLOCKS_PER_SEC;
    err = calc_errors(x*N, sum);

    printf("recursive sum: %f\n", sum);
    printf("absolute error: %f\n", err.absolute);
    printf("relative error: %f = %f%%\n", err.relative, err.relative * 100);
    printf("%f s\n\n", seconds);

    c = clock();
    sum = sum_kahana(t, N);
    c = clock() - c;
    seconds = ((double) c) / CLOCKS_PER_SEC;
    err = calc_errors(x*N, sum);

    printf("Kahan sum: %f\n", sum);
    printf("absolute error: %f\n", err.absolute);
    printf("relative error: %f = %f%%\n", err.relative, err.relative * 100);
    printf("%f s\n\n", seconds);

    for (int i = 0; i < N; i++) {
        t[i] = i / ((float) N);
    }
    sum = sum_recursive(t, N);
    err = calc_errors((t[0] + t[N-1]) * (N / 2.0), sum);
    printf("recursive sum: %f\n", sum);
    printf("absolute error: %f\n", err.absolute);
    printf("relative error: %f = %f%%\n", err.relative, err.relative * 100);

    free(t);
    return 0;
}
