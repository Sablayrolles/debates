#!/bin/bash

# echo -e "\t\t\t\t Compilation du rapport :: usage $0 [-v]\n\n\t-v :: verbose mode\n\n"
# echo -e "Preparation\n\ti.Traitement graphes..."
# cd images/
# rm *.log >/dev/null 2>/dev/null
# for fic in `ls -1 | grep ".dot"`; do
	# name=${fic%%.*}
	# echo -e "\t\tConverting $fic to $name.png"
	# dot -Tpng -o$name.png $fic
	# echo -e "\t\tChanging in report.tex"
	# sed -i -e "s/$fic/$name.png/g" ../report.tex >/dev/null 2>/dev/null
# done
# echo -e "\n\tDone\n\t2.Traitement des images"
# for fic in `ls -1 | grep -v ".eps" | grep -v ".txt" | grep -v ".dot"`; do
	# name=${fic%%.*}
	# echo -e "\t\tConverting $fic to $name.eps"
	# convert $fic eps2:$name.eps >/dev/null 2>/dev/null
	# echo -e "\t\tChanging in report.tex"
	# sed -i -e "s/$fic/$name.eps/g" ../report.tex >/dev/null 2>/dev/null
# done
# echo -e "\tDone.\nReady to compile.\n\n"
# cd ../

echo -e "Compilation du rapport\n\t1.Precompilation latex..."
if [ -n $1 ] && [ "$1" == "-v" ]; then
	timeout 40 latex travail.tex
else
	latex travail.tex 2>/dev/null >/dev/null
fi
echo -e "\tDone.\n\t"

read -p "Continue? [o/n] " -t 3 c
if [ "$c" == "n" ]; then
	exit 1;
fi

echo -e "\n\n\t2.Compilation bibiliographie..."
bibtex travail >/dev/null
# echo -e "\tDone.\n\t3.Compilation index abreviations..."
# makeindex report.glo -t report.glg -s report.ist -o report.gls >/dev/null 2>/dev/null
echo -e "\tDone.\n\t4.Compilation latex to dvi (first step)..."
latex travail 2>/dev/null >/dev/null
echo -e "\tDone.\n\t5.Compilation latex to dvi (second step)..."
latex travail 2>/dev/null >/dev/null
echo -e "\tDone.\n\t6.Compilation dvi to ps..."
dvips travail.dvi >/dev/null 2>/dev/null
echo -e "\tDone.\n\t7.Compilation ps to pdf..."
ps2pdf travail.ps travail.pdf >/dev/null

tmp=`ls travail.{aux,bbl,blg,idx,ilg,ind,dvi,glg,glo,gls,glsdefs,ist,lof,lot,out,ps,toc} 2>/dev/null`
nbfic=`echo $tmp | wc -w`
echo -e "\tDone.\nCompilation finished.\nCleaning temp files[$nbfic]..."
rm -f $tmp
