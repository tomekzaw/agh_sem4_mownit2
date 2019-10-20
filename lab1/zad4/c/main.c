#include <stdio.h>

int count_iter(float x, float r, float epsilon, float threshold) {
	int i = 0;
	while (x > epsilon) {
		if (i > threshold) {
			return -1;
        }
		x = r * x * (1-x);
        i++;
    }
	return i;
}
 
int main(int argc, char** argv) {
    for (float x = 0.0f; x <= 1.0f; x += 0.01f) {
        printf("%f\t%d\n", x, count_iter(x, 4.0f, 1e-9, 1e7));
    }
    return 0;
}