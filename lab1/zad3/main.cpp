#include <iostream>
#include <cmath>
#include <cstdio>

using namespace std;

float minus_one_to(int k) {
    return (k % 2 ? -1.0f : 1.0f);
}

float dzeta_float_forward(float s, int n) {
    float result = 0.0f;
    for (int k = 1; k <= n; k++) {
        result += 1 / pow(k, s);
    }
    return result;
}

float dzeta_float_backward(float s, int n) {
    float result = 0.0f;
    for (int k = n; k >= 1; k--) {
        result += 1 / pow(k, s);
    }
    return result;
}

double dzeta_double_forward(double s, int n) {
    double result = 0.0;
    for (int k = 1; k <= n; k++) {
        result += 1 / pow(k, s);
    }
    return result;
}

double dzeta_double_backward(double s, int n) {
    double result = 0.0f;
    for (int k = n; k >= 1; k--) {
        result += 1 / pow(k, s);
    }
    return result;
}

float eta_float_forward(float s, int n) {
    float result = 0.0f;
    for (int k = 1; k <= n; k++) {
        result += minus_one_to(k-1) / pow(k, s);
    }
    return result;
}

float eta_float_backward(float s, int n) {
    float result = 0.0f;
    for (int k = n; k >= 1; k--) {
        result += minus_one_to(k-1) / pow(k, s);
    }
    return result;
}

double eta_double_forward(double s, int n) {
    double result = 0.0;
    for (int k = 1; k <= n; k++) {
        result += minus_one_to(k-1) / pow(k, s);
    }
    return result;
}

double eta_double_backward(double s, int n) {
    double result = 0.0f;
    for (int k = n; k >= 1; k--) {
        result += minus_one_to(k-1) / pow(k, s);
    }
    return result;
}

int main() {
    double ss[] = {2, 3.6667, 5, 7.2, 10};
    int sc = sizeof(ss) / sizeof(ss[0]);

    int ns[] = {50, 100, 200, 500, 1000};
    int nc = sizeof(ns) / sizeof(ns[0]);

    printf("%5s%7s%20s%20s%20s%20s\n", "s", "n", "float forward", "float backward", "double forward", "double backward");
    for (int si = 0; si < sc; si++) {
        printf("\n");
        double s = ss[si];
        for (int ni = 0; ni < nc; ni++) {
            int n = ns[ni];
            printf("%5.2f%7d%20.16g%20.16g%20.16g%20.16g\n",
                s, n,
                dzeta_float_forward(s, n),
                dzeta_float_backward(s, n),
                dzeta_double_forward(s, n),
                dzeta_double_backward(s, n)
            );
        }
    }

    printf("\n\n");
    printf("%5s%7s%20s%20s%20s%20s\n", "s", "n", "float forward", "float backward", "double forward", "double backward");
    for (int si = 0; si < sc; si++) {
        printf("\n");
        double s = ss[si];
        for (int ni = 0; ni < nc; ni++) {
            int n = ns[ni];
            printf("%5.2f%7d%20.16g%20.16g%20.16g%20.16g\n",
                s, n,
                eta_float_forward(s, n),
                eta_float_backward(s, n),
                eta_double_forward(s, n),
                eta_double_backward(s, n)
            );
        }
    }

    return 0;
}
