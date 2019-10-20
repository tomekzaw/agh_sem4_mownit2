plot: bifur	
	mkdir -p dat png
	for x in "" 0.1 0.25 0.5 0.85 ; do \
		./bifur $$x > dat/bifur$$x.dat ; \
		gnuplot -e "in='dat/bifur$$x.dat'" -e "out='png/bifur$$x.png'" -e "color='blue'" bifur.gnuplot ; \
	done
 
bifur: bifur.o
	gcc -o bifur bifur.o
 
bifur.o: bifur.c
	gcc -c -Wall bifur.c
 
clean:
	rm -rf *.o bifur dat png