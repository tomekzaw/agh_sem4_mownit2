#include <stdlib.h>
#include <stdio.h>

int main(int argc, char** argv) {
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

    float sum = 0.0f;
    for (int i = 0; i < N; i++) {
        if (i % 25000 == 0) {
            float exact = i*x;
            float err = abs(exact - sum) / exact;
            printf("%d\t%f\n", i, err);
        }
        sum += t[i];
    }
    
    free(t);
    return 0;
}
