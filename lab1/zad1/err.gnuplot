#!/usr/bin/gnuplot -persist

set terminal pngcairo size 800,600
set output 'err.png'
plot 'err.dat' with lines linewidth 2 linecolor rgb "red" notitle