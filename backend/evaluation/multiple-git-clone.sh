#!/bin/sh

# Modified from: https://gist.github.com/benizar/03c5ede574ac7b847413857f74bb04b3

cat repositories.txt | while read line
do
   git clone $line
done