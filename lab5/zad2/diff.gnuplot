#!/usr/bin/gnuplot -persist

set terminal pngcairo size 800,600
#set logscale y
set output 'diff.png'
plot 'diff.dat' with lines linewidth 2 linecolor rgb "red" notitle