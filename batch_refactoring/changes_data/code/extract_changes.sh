#!/usr/bin/env bash
for i in $(cat export_industry.csv); do
	folder=$(echo $i | cut -d "," -f 1)	
	out_file="$HOME/PycharmProjects/scripts_cedrim/batch_refactoring/changes_data/whatchanged_${folder}.txt"
	git -C "repos/${folder}" log --pretty="commit=%H:%ae" --name-status > ${out_file}
done