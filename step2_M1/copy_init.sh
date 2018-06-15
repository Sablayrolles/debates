#!/bin/sh

for f in `ls`; do
	if [ -d $f ]; then
		echo "Copying __init__.py  to "$f;
		a="cp ./__init__.py ./$f/__init__.py";
		echo $a`$a`;
	fi;
done;