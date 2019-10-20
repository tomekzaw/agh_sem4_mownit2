main: main.o
	gcc -o main main.o
 
main.o: main.c
	gcc -c -Wall main.c
 
clean:
	rm -rf *.o main

plot: main
	./main > main.dat
	gnuplot main.gnuplot