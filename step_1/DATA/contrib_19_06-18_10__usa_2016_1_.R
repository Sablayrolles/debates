library(ggplot2) # R (command pour lancer la console R) install.packages("ggplot2")
#Rscript name.R pour compiler

name = "Contribution" #lambda ou methode ou contribution
param_fix = "Methode-2_Lambda-1_q2**19_06-18_07__usa_2016_1_" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = "num_EDU"
legend_y_axis = "Score"
ptn_size = 12


x=c( 8, 9, 10, 11, 12, 14, 31, 32, 34, 35, 36, 37, 42, 43, 44)
lambda=c(, 0.43046721, 0.387420489, 0.3486784401, 0.31381059609, 0.282429536481, 0.22876792455, 0.0381520424477, 0.0343368382029, 0.0278128389444, 0.0250315550499, 0.0225283995449, 0.0202755595904, 0.0119725151826, 0.0107752636643, 0.00969773729788)
score=c(0.00193954745958)

nb_val = length(x)
size = 0:(nb_val-1)

png(file=paste(name, "_Score_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste(name, "_Score_", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=lambda, colour="lambda"))
	+geom_line(aes(x=x, y=score, colour="score"))
	+geom_point(aes(x=x, y=lambda, colour="lambda"))
	+geom_point(aes(x=x, y=score, colour="score"))
)
dev.off()
#------------------------------------------------------------------


name = "Contribution" #lambda ou methode ou contribution
param_fix = "Methode-3_Lambda-1_q2**19_06-18_08__usa_2016_1_" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = "num_EDU"
legend_y_axis = "Score"
ptn_size = 12


x=c( 8, 9, 10, 11, 12, 14, 31, 32, 34, 35, 36, 37, 42, 43, 44)
lambda=c(, 0.43046721, 0.387420489, 0.3486784401, 0.31381059609, 0.282429536481, 0.22876792455, 0.0381520424477, 0.0343368382029, 0.0278128389444, 0.0250315550499, 0.0225283995449, 0.0202755595904, 0.0119725151826, 0.0107752636643, 0.00969773729788)
score=c(0.00290932118936)

nb_val = length(x)
size = 0:(nb_val-1)

png(file=paste(name, "_Score_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste(name, "_Score_", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=lambda, colour="lambda"))
	+geom_line(aes(x=x, y=score, colour="score"))
	+geom_point(aes(x=x, y=lambda, colour="lambda"))
	+geom_point(aes(x=x, y=score, colour="score"))
)
dev.off()
#------------------------------------------------------------------


name = "Contribution" #lambda ou methode ou contribution
param_fix = "Methode-2_Lambda-0.95_q2**19_06-18_08__usa_2016_1_" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = "num_EDU"
legend_y_axis = "Score"
ptn_size = 12


x=c( 8, 9, 10, 11, 12, 14, 31, 32, 34, 35, 36, 37, 42, 43, 44)
lambda=c(, 0.43046721, 0.387420489, 0.3486784401, 0.31381059609, 0.282429536481, 0.22876792455, 0.0381520424477, 0.0343368382029, 0.0278128389444, 0.0250315550499, 0.0225283995449, 0.0202755595904, 0.0119725151826, 0.0107752636643, 0.00969773729788)
score=c(0.00193954745958)

nb_val = length(x)
size = 0:(nb_val-1)

png(file=paste(name, "_Score_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste(name, "_Score_", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=lambda, colour="lambda"))
	+geom_line(aes(x=x, y=score, colour="score"))
	+geom_point(aes(x=x, y=lambda, colour="lambda"))
	+geom_point(aes(x=x, y=score, colour="score"))
)
dev.off()
#------------------------------------------------------------------


name = "Contribution" #lambda ou methode ou contribution
param_fix = "Methode-3_Lambda-0.95_q2**19_06-18_09__usa_2016_1_" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = "num_EDU"
legend_y_axis = "Score"
ptn_size = 12


x=c( 8, 9, 10, 11, 12, 14, 31, 32, 34, 35, 36, 37, 42, 43, 44)
lambda=c(, 0.43046721, 0.387420489, 0.3486784401, 0.31381059609, 0.282429536481, 0.22876792455, 0.0381520424477, 0.0343368382029, 0.0278128389444, 0.0250315550499, 0.0225283995449, 0.0202755595904, 0.0119725151826, 0.0107752636643, 0.00969773729788)
score=c(0.00290932118936)

nb_val = length(x)
size = 0:(nb_val-1)

png(file=paste(name, "_Score_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste(name, "_Score_", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=lambda, colour="lambda"))
	+geom_line(aes(x=x, y=score, colour="score"))
	+geom_point(aes(x=x, y=lambda, colour="lambda"))
	+geom_point(aes(x=x, y=score, colour="score"))
)
dev.off()
#------------------------------------------------------------------


