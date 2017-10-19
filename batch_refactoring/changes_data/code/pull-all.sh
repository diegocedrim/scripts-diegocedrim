#!/usr/bin/env bash
for i in $(cat export_industry.csv); do
	name=$(echo $i | cut -d "," -f 1)
	url=$(echo $i | cut -d "," -f 2)
	git clone $url repos/$name
done