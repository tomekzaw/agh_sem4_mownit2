#!/usr/bin/gnuplot -persist

set terminal pngcairo size 1200,600
set output 'main.png'
set key outside
plot for [col=2:3] 'main.dat' using 0:col with lines linewidth 2 title columnheader