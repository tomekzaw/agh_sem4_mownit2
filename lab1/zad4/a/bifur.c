#include <stdlib.h>
#include <stdio.h>
 
int main(int argc, char** argv) {    
    const double r_min = 1.0, r_max = 4.0, r_step = 1e-3, x0 = (argc >= 2 ? atof(argv[1]) : 0.5);
    const int i_min = (argc >= 2 ? 0 : 100), i_max = 800;

    for (double r = r_min; r < r_max; r += r_step) {
        double x = x0;
        for (int i = 0; i <= i_max; i++) {
            if (i >= i_min) {
                printf("%f\t%f\n", r, x);
            }
            x = r*x*(1-x);
        }
    }
    return 0;
}