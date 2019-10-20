#!/usr/bin/gnuplot -persist

set logscale xy 2
set mytics 16
set mxtics 8
set key left top
set xlabel "{/Helvetica-Italic n}"
set ylabel "{/Helvetica-Italic t} [s]"
set terminal pngcairo size 960,640
set output 'compare.png'
plot 'compare.dat' using 1:2 pointsize 1 pointtype 2 linecolor rgb "red" title "zad1.solve\\\_gauss\\\_jordan", \
    'compare.dat' using 1:3 pointsize 1 pointtype 1 linecolor rgb "blue" title "numpy.linalg.solve"