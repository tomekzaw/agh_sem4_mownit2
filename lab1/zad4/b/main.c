#include <stdlib.h>
#include <stdio.h>
 
int main(int argc, char** argv) {    
    double x_double = 0.25;
    float x_float = (float) x_double;
    double r = 3.8;
    printf("i\tfloat\t\tdouble\n");
    for (int i = 0; i <= 50; i++) {
        printf("%d\t%f\t%f\n", i, x_float, x_double);
        x_float = ((float) r) * x_float * (1 - x_float);
        x_double = r * x_double * (1 - x_double);        
    }
    return 0;
}