#!/bin/bash

debug=0

if [ -f ./scripts/config/rapid.txt ]; then
	echo -e "\e[1;36m[Scoring]\e[0m Recuperation des scores"
	echo -e "\e[1;36m[Scoring]\e[0m Old config found..."
	nb_lig=`cat ./scripts/config/rapid.txt | wc -l`
	for i in `seq 1 $nb_lig`; do
		lig=`cat ./scripts/config/rapid.txt | head -$i | tail -1 `
		echo -e "\e[1;36m[Scoring]\e[0m "$lig
	done;
	echo -e "\e[1;36m[Scoring]\e[0m Keep same [y/n]?"
	read keep
else
	keep="n"
fi;
																						keep="y"
if [ $keep == "y" ]; then
	param=`head -1 ./scripts/config/rapid.txt | cut -d: -f2`
	method=`head -2 ./scripts/config/rapid.txt | tail -1 | cut -d: -f2`
	lambda=`head -3 ./scripts/config/rapid.txt | tail -1 | cut -d: -f2`
	corpus=`head -4 ./scripts/config/rapid.txt | tail -1 | cut -d: -f2`
	names=`head -5 ./scripts/config/rapid.txt | tail -1 | cut -d: -f2`
	fic=`head -6 ./scripts/config/rapid.txt | tail -1 | cut -d: -f2`
else
	echo -e "\e[1;36m[Scoring]\e[0m Recuperation des scores"
	read -p 'Notations a traiter (H:hand, S:script, "": both, c:contrib): ' param
	read -p "Num methodes (,:sep;max=7): " method
	read -p "Lambda to test (,:sep):  " lambda
	read -p "Path of the corpus: " corpus
	read -p "Names of the candidat to look ( :sep): " names
	read -p "Name output fic: " fic
	read -p "Save [y/n]? " save
	if [ "$save" == "y" ]; then
		echo "param:$param">./scripts/config/rapid.txt
		echo "method:$method">>./scripts/config/rapid.txt
		echo "lambda:$lambda">>./scripts/config/rapid.txt
		echo "corpus:$corpus">>./scripts/config/rapid.txt
		echo "names:$names">>./scripts/config/rapid.txt
		echo "fic:$fic">>./scripts/config/rapid.txt
	fi
fi

dataset=`echo $corpus | sed "s/\.\//_/g" | sed "s/\//_/g"`

# if [ $debug -eq 1 ]; then
	# if [ -n $param ]; then
		# echo -e "\e[1;36m[Scoring]\e[0m bash -x ./scripts/notations/get_scoring.sh $param $method $lambda $corpus \"$names\" fic"
		# res_fic_save=`bash -x ./scripts/notations/get_scoring.sh $param $method $lambda $corpus "$names" fic | tail -1`
	# else
		# echo -e "\e[1;36m[Scoring]\e[0m bash -x  ./scripts/notations/get_scoring.sh $method $lambda $corpus \"$names\" fic"
		# res_fic_save=`bash -x ./scripts/notations/get_scoring.sh $method $lambda $corpus "$names" fic | tail -1`
	# fi
# else
	# if [ -n $param ]; then
		# echo -e "\e[1;36m[Scoring]\e[0m ./scripts/notations/get_scoring.sh $param $method $lambda $corpus \"$names\" fic"
		# res_fic_save=`./scripts/notations/get_scoring.sh $param $method $lambda $corpus "$names" fic | tail -1`
	# else
		# echo -e "\e[1;36m[Scoring]\e[0m ./scripts/notations/get_scoring.sh $method $lambda $corpus \"$names\" fic"
		# res_fic_save=`./scripts/notations/get_scoring.sh $method $lambda $corpus "$names" fic | tail -1`
	# fi
# fi

if [ `echo $lambda | grep "," | wc -l` -ne 0 ]; then
	nbL=1
	cmd=`echo $lambda | cut -d\, -f$nbL`
	while [ "$cmd" != "" ]; do
		let "nbL=$nbL+1"
		cmd=`echo $lambda | cut -d\, -f$nbL`
	done;
	let "nbL=$nbL-1"
else
	nbL=1
	old_lambda=$lambda
	lambda=$lambda","
fi
if [ `echo $names | grep ' ' | wc -l` -ne 0 ]; then	
	nbN=1
	cmd=`echo $names | cut -d' ' -f$nbN`
	while [ "$cmd" != "" ]; do
		let "nbN=$nbN+1"
		cmd=`echo $names | cut -d' ' -f$nbN`
	done;
	let "nbN=$nbN-1"
else
	nbN=1
	names=$names","
fi
if [ `echo $method | grep "," | wc -l` -ne 0 ]; then	
	nbM=1
	cmd=`echo $method | cut -d\, -f$nbM`
	while [ "$cmd" != "" ]; do
		let "nbM=$nbM+1"
		cmd=`echo $method | cut -d\, -f$nbM`
	done;
	let "nbM=$nbM-1"
else
	nbM=1
	method=$method","
fi

echo -e "\e[1;94m[Output]\e[0m Recuperation sortie des resultats (help : help)"
read -p "[Output] " cmd
while [ "$cmd" != "quit" ]; do
	if [ "$cmd" == "help" ]; then
		echo -e "\e[1;94m[Output]\e[0m help : affiche l'aide"
		echo -e "\e[1;94m[Output]\e[0m latex lambda : export les resultats des scores en fonctions des lambdas sous forme de tableau latex"
		echo -e "\e[1;94m[Output]\e[0m latex method : export les resultats des scores en fonctions des methodes sous forme de tableau latex"
		echo -e "\e[1;94m[Output]\e[0m graph lambda xxx : export les resultats des scores en fonctions des lambdas sous forme de graphique"
		echo -e "\e[1;94m[Output]\e[0m graph method xxx : export les resultats des scores en fonctions des methodes sous forme de graphique"
		if [ `echo $param | grep "c" | wc -l` -eq 1 ]; then
			echo -e "\e[1;94m[Output]\e[0m graph contrib xxx num_q nb_max_ptn : export les resultats des contributions en fonctions des EDU sous forme de graphique"
		fi;
		echo -e "\e[1;94m[Output]\e[0m quit : quitte le programme\n"
		echo -e "\e[1;94m[Output]\e[0m xxx : type de courbe {ptn,line,ptnline}"
		echo -e "\e[1;94m[Output]\e[0m num_q : numero de la question a recuperer"
		echo -e "\e[1;94m[Output]\e[0m nb_max_ptn : 2s/ptn/lambda/method"
	fi;
	if [ `echo $cmd | grep "graph" | wc -l` -eq 1 ]; then
		if [ `echo $cmd | grep "lambda" | wc -l` -eq 1 ]; then
			echo 'library(ggplot2) # R (command pour lancer la console R) install.packages("ggplot2")'>graph.R
			echo '#Rscript name.R pour compiler'>>graph.R
			echo ''>>graph.R
			a=1
			while [ $a -le $nbM ]; do
				methoD=`echo $method | cut -d\, -f$a`
				echo 'name = "Lambda" #lambda ou methode'>>graph.R
				date=`date "+%d_%m-%H_%M"`
				echo 'param_fix = "Methode-'$methoD'_'$date'_'$dataset'" #parametre fixe avec valeur'>>graph.R
				echo 'background = "white"'>>graph.R
				echo 'size_x = 720'>>graph.R
				echo 'size_y = 480'>>graph.R
				echo 'legend_x_axis = name'>>graph.R
				echo 'legend_y_axis = "Score"'>>graph.R
				echo 'ptn_size = 12'>>graph.R
				echo ''>>graph.R
				echo 'x=c('$lambda')'>>graph.R
				b=1
				while [ $b -le $nbN ]; do
					name=`echo $names | cut -d' ' -f$b`
					echo 'name_y'$b'="'$name'"'>>graph.R
					c=1
					ch=""
					while [ $c -le $nbL ]; do
						lambdA=`echo $lambda | cut -d\, -f$c`
						#echo "cat $res_fic_save | grep \"($methoD,$name,$lambdA\" | cut -d, -f4 | cut -d\) -f1"
						score=`cat $res_fic_save | grep "($methoD,$name,$lambdA," | cut -d, -f4 | cut -d\) -f1`
						if [ $c -eq 1 ]; then
							ch=$score
						else
							ch=$ch","$score
						fi
						let "c=$c+1"
					done
					echo 'y'$b'=c('$ch')'>>graph.R
					let "b=$b+1"
				done;
				echo ''
				echo 'nb_val = length(y1)'>>graph.R
				echo 'size = 0:(nb_val-1)'>>graph.R
				echo ''>>graph.R
				echo 'png(file=paste("Variation_Scores_", name, "_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)'>>graph.R
				echo '(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))'>>graph.R
				echo '	+xlab(legend_x_axis)'>>graph.R
				echo '	+ylab(legend_y_axis)'>>graph.R
				echo '	+expand_limits(x=c(min(x),max(x)))'>>graph.R
				echo '	+ggtitle(paste("Variation Scores ", name, " ", param_fix, sep=""))'>>graph.R
				echo '	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))'>>graph.R
				echo '	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)'>>graph.R
				b=1
				while [ $b -le $nbN ]; do
					name=`echo $names | cut -d' ' -f$b`{ptn,line,ptnline}
					if [ `echo $cmd | grep "line" | wc -l` -eq 1 -o `echo $cmd | grep -v "ptn" | wc -l` -eq 1 ]; then
						echo '	+geom_line(aes(x=x, y=y'$b', colour=name_y'$b'))'>>graph.R
					fi;
					if [ `echo $cmd | grep "ptn" | wc -l` -eq 1 -o `echo $cmd | grep -v "line" | wc -l` -eq 1 ]; then
						echo '	+geom_point(aes(x=x, y=y'$b', colour=name_y'$b'))'>>graph.R
					fi;
					let "b=$b+1"
				done;
				echo '	+scale_colour_discrete(name="Names",'>>graph.R
				echo '		breaks=c(NULL'>>graph.R
				b=1
				while [ $b -le $nbN ]; do
					name=`echo $names | cut -d' ' -f$b`
					echo '		,name_y'$b''>>graph.R
					let "b=$b+1"
				done;
				echo '		)'>>graph.R
				echo '		, labels=c(NULL'>>graph.R
				b=1
				while [ $b -le $nbN ]; do
					name=`echo $names | cut -d' ' -f$b`
					echo '		,name_y'$b''>>graph.R
					let "b=$b+1"
				done;
				echo '		)'>>graph.R
				echo '	)'>>graph.R
				echo ')'>>graph.R
				echo 'dev.off()'>>graph.R
				echo '#------------------------------------------------------------------'>>graph.R
				echo ''>>graph.R
				echo ''>>graph.R
				
				let "a=$a+1"
			done;
			Rscript graph.R
			date=`date "+%d_%m-%H_%M"`
			name="graph_lambda_"$date"_"$dataset".R"
			mv graph.R $name
		fi;
		if [ `echo $cmd | grep "method" | wc -l` -eq 1 ]; then
			echo 'library(ggplot2) # R (command pour lancer la console R) install.packages("ggplot2")'>graph.R
			echo '#Rscript name.R pour compiler'>>graph.R
			echo ''>>graph.R
			a=1
			while [ $a -le $nbL ]; do
				lambdA=`echo $lambda | cut -d\, -f$a`
				echo 'name = "Methode" #lambda ou methode'>>graph.R
				date=`date "+%d_%m-%H_%M"`
				echo 'param_fix = "Lambda-'$lambdA'_'$date'_'$dataset'" #parametre fixe avec valeur'>>graph.R
				echo 'background = "white"'>>graph.R
				echo 'size_x = 720'>>graph.R
				echo 'size_y = 480'>>graph.R
				echo 'legend_x_axis = name'>>graph.R
				echo 'legend_y_axis = "Score"'>>graph.R
				echo 'ptn_size = 12'>>graph.R
				echo ''>>graph.R
				echo 'x=c('$method')'>>graph.R
				b=1
				while [ $b -le $nbN ]; do
					name=`echo $names | cut -d' ' -f$b`
					echo 'name_y'$b'="'$name'"'>>graph.R
					c=1
					ch=""
					while [ $c -le $nbM ]; do
						methoD=`echo $method | cut -d\, -f$c`
						#echo "cat $res_fic_save | grep \"($methoD,$name,$lambdA\" | cut -d, -f4 | cut -d\) -f1"
						score=`cat $res_fic_save | grep "($methoD,$name,$lambdA," | cut -d, -f4 | cut -d\) -f1`
						if [ $c -eq 1 ]; then
							ch=$score
						else
							ch=$ch","$score
						fi
						let "c=$c+1"
					done
					echo 'y'$b'=c('$ch')'>>graph.R
					let "b=$b+1"
				done;
				echo ''
				echo 'nb_val = length(y1)'>>graph.R
				echo 'size = 0:(nb_val-1)'>>graph.R
				echo ''>>graph.R
				echo 'png(file=paste("Variation_Scores_", name, "_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)'>>graph.R
				echo '(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))'>>graph.R
				echo '	+xlab(legend_x_axis)'>>graph.R
				echo '	+ylab(legend_y_axis)'>>graph.R
				echo '	+expand_limits(x=c(min(x),max(x)))'>>graph.R
				echo '	+ggtitle(paste("Variation Scores ", name, " ", param_fix, sep=""))'>>graph.R
				echo '	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))'>>graph.R
				echo '	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)'>>graph.R
				b=1
				while [ $b -le $nbN ]; do
					name=`echo $names | cut -d' ' -f$b`
					if [ `echo $cmd | grep "line" | wc -l` -eq 1 -o `echo $cmd | grep -v "ptn" | wc -l` -eq 1 ]; then
						echo '	+geom_line(aes(x=x, y=y'$b', colour=name_y'$b'))'>>graph.R
					fi;
					if [ `echo $cmd | grep "ptn" | wc -l` -eq 1 -o `echo $cmd | grep -v "line" | wc -l` -eq 1 ]; then
						echo '	+geom_point(aes(x=x, y=y'$b', colour=name_y'$b'))'>>graph.R
					fi;
					let "b=$b+1"
				done;
				echo '	+scale_colour_discrete(name="Names",'>>graph.R
				echo '		breaks=c(NULL'>>graph.R
				b=1
				while [ $b -le $nbN ]; do
					name=`echo $names | cut -d' ' -f$b`
					echo '		,name_y'$b''>>graph.R
					let "b=$b+1"
				done;
				echo '		)'>>graph.R
				echo '		, labels=c(NULL'>>graph.R
				b=1
				while [ $b -le $nbN ]; do
					name=`echo $names | cut -d' ' -f$b`
					echo '		,name_y'$b''>>graph.R
					let "b=$b+1"
				done;
				echo '		)'>>graph.R
				echo '	)'>>graph.R
				echo ')'>>graph.R
				echo 'dev.off()'>>graph.R
				echo '#------------------------------------------------------------------'>>graph.R
				echo ''>>graph.R
				echo ''>>graph.R
				
				let "a=$a+1"
			done;
			Rscript graph.R
			date=`date "+%d_%m-%H_%M"`
			name="graph_lambda_"$date"_"$dataset".R"
			mv graph.R $name
		fi;
		if [ `echo $param | grep "c" | wc -l` -eq 1 ]; then
			if [ `echo $cmd | grep "contrib" | wc -l` -eq 1 ]; then
				numq=`echo $cmd | cut -d" " -f4`
				maxptn=`echo $cmd | cut -d" " -f5`
				echo 'library(ggplot2) # R (command pour lancer la console R) install.packages("ggplot2")'>graph.R
				echo '#Rscript name.R pour compiler'>>graph.R
				echo ''>>graph.R
				lamb=1
				while [ $lamb -le $nbL ]; do
					lambdA=`echo $lambda | cut -d\, -f$lamb`
					# echo "l"$lamb
					met=1
					while [ $met -le $nbM ]; do
						# echo "m"$met
						methoD=`echo $method | cut -d\, -f$met`
						nameFic="M"$methoD"L"$lambdA".contrib"
						if [ -e "$nameFic" ]; then
							echo 'name = "Contribution" #lambda ou methode ou contribution'>>graph.R
							date=`date "+%d_%m-%H_%M"`
							echo 'param_fix = "Methode-'$methoD'_Lambda-'$lambdA'_q'$numq'**'$date'_'$dataset'" #parametre fixe avec valeur'>>graph.R
							echo 'background = "white"'>>graph.R
							echo 'size_x = 720'>>graph.R
							echo 'size_y = 480'>>graph.R
							echo 'legend_x_axis = "num_EDU"'>>graph.R
							echo 'legend_y_axis = "Score"'>>graph.R
							echo 'ptn_size = 12'>>graph.R
							echo ''>>graph.R
							nameFic="M"$methoD"L"$lambdA".contrib"
							nums_EDU=""
							Lambda=""
							Score=""
							entete="M"$methoD"L"$lambdA
							nb=0
							nblig=`cat $nameFic | grep "$entete" | grep "Q.$numq" | wc -l`
							echo ""
							while [ $nb -le $nblig ] && [ $nb -le $maxptn ] ; do
								let "nb=$nb+1"
								lig=`cat $nameFic | grep "$entete" | grep "Q.$numq" | head -$nb | tail -1`
								let "aff=$nb-1"
								echo -e "\e[1A\e[1;94m[Output]\e[0m Lecture des donnees ............ "$aff" / "$maxptn
								num=`echo -e $lig | cut -f1 | cut -d\- -f2 | cut -d\/ -f1`
								val_l=`echo -e $lig | cut -d" " -f2 | cut -d\: -f2`
								val_s=`echo -e $lig | cut -d" " -f4 | cut -d\: -f2`
								# echo "recup:"$num", "$val_l", "$val_s
								if [ `echo $nums_EDU | grep " $num" | wc -l` -eq 0 ]; then
									if [ "$nums_EDU" == "" ]; then
										nums_EDU=" "$num
									else
										nums_EDU=$nums_EDU", "$num
									fi
									if [ $nb -eq 1 ]; then
										Lambda=$val_l
									else
										Lambda=$Lambda", "$val_l
									fi
									if [ -z "$score" ]; then
										Score=$val_s
									else
										Score=$Score", "$val_s
									fi
								fi
							done;
							echo ''>>graph.R
							echo 'x=c('$nums_EDU')'>>graph.R
							
							echo 'lambda=c('$Lambda')'>>graph.R
							echo 'score=c('$Score')'>>graph.R
							
							echo ''>>graph.R
							echo 'nb_val = length(x)'>>graph.R
							echo 'size = 0:(nb_val-1)'>>graph.R
							echo ''>>graph.R
							echo 'png(file=paste(name, "_Score_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)'>>graph.R
							echo '(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))'>>graph.R
							echo '	+xlab(legend_x_axis)'>>graph.R
							echo '	+ylab(legend_y_axis)'>>graph.R
							echo '	+expand_limits(x=c(min(x),max(x)))'>>graph.R
							echo '	+ggtitle(paste(name, "_Score_", param_fix, sep=""))'>>graph.R
							echo '	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))'>>graph.R
							echo '	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)'>>graph.R
							if [ `echo $cmd | grep "line" | wc -l` -eq 1 -o `echo $cmd | grep -v "ptn" | wc -l` -eq 1 ]; then
								echo '	+geom_line(aes(x=x, y=lambda, colour="lambda"))'>>graph.R
								echo '	+geom_line(aes(x=x, y=score, colour="score"))'>>graph.R
							fi;
							if [ `echo $cmd | grep "ptn" | wc -l` -eq 1 -o `echo $cmd | grep -v "line" | wc -l` -eq 1 ]; then
								echo '	+geom_point(aes(x=x, y=lambda, colour="lambda"))'>>graph.R
								echo '	+geom_point(aes(x=x, y=score, colour="score"))'>>graph.R
							fi;
							echo ')'>>graph.R
							echo 'dev.off()'>>graph.R
							echo '#------------------------------------------------------------------'>>graph.R
							echo ''>>graph.R
							echo ''>>graph.R
						else
							echo $nameFic" doesn't exist"
						fi;
						let "met=$met+1"
					done;
					let "lamb=$lamb+1"
				done;
				Rscript graph.R
				date=`date "+%d_%m-%H_%M"`
				name="contrib_"$date"_"$dataset".R"
				mv graph.R $name
			fi;
		fi;
	fi;
 
	read -p "[Output] " cmd
done;

rm fic *.result *.contrib 2>/dev/null
mv *.R ./scripts/notations/result/Rscripts/ 2>/dev/null
mv *.png ./scripts/notations/result/imgs/ 2>/dev/null

