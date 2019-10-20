#!/usr/bin/gnuplot -persist

if (!exists("in")) in="bifur.dat"
if (!exists("out")) out="bifur.png"
if (!exists("color")) color="blue"

set terminal pngcairo size 1080,720
set output out
plot in with points pointtype 2 pointsize 0.01 linecolor rgb color notitle