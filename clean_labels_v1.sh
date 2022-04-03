#!/bin/bash

sed -i -e '1,39d' ./my_labels.txt

sed -i '
  :loop
  $b
  N
  /\ldi\nldi/d
  P
  s/.*\n//
  b loop
 ' ./my_labels.txt

sed -i '/nop/d' ./my_labels.txt 


sed -i '/sbi_1/d' ./my_labels.txt
sed -i '/cbi/d' ./my_labels.txt

sed -i '/sleep/d'  ./my_labels.txt