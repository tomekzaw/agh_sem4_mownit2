main: main.o
	gcc -o main main.o
 
main.o: main.c
	gcc -c -Wall main.c

err: err.o
	gcc -o err err.o
 
err.o: err.c
	gcc -c -Wall err.c

plot: err
	./err > err.dat
	gnuplot err.gnuplot
 
clean:
	rm -rf *.o *.dat *.png main err
