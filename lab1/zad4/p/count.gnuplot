#!/usr/bin/gnuplot -persist

set terminal pngcairo size 1080,720
set output 'count.png'
set key outside
plot 'count.dat' with points pointtype 7 pointsize 0.25 linewidth 2 notitle