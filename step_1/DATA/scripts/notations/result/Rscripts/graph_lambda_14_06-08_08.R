library(ggplot2) # R (command pour lancer la console R) install.packages("ggplot2")
#Rscript name.R pour compiler

name = "Lambda" #lambda ou methode
param_fix = "Methode-2_14_06-08_06" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = name
legend_y_axis = "Score"
ptn_size = 12

x=c(1,0.95,0.9,0.85,0.8,0.75,0.7)
name_y1="CLINTON"
y1=c(0.6907177610498181,0.6907177610498181,0.6907177610498181,0.6907177610498181,0.6907177610498181,0.6907177610498181,0.6907177610498181)
name_y2="TRUMP"
y2=c(0.42420017575101704,0.42420017575101704,0.42420017575101704,0.42420017575101704,0.42420017575101704,0.42420017575101704,0.42420017575101704)
nb_val = length(y1)
size = 0:(nb_val-1)

png(file=paste("Variation_Scores_", name, "_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste("Variation Scores ", name, " ", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=y1, colour=name_y1))
	+geom_point(aes(x=x, y=y1, colour=name_y1))
	+geom_line(aes(x=x, y=y2, colour=name_y2))
	+geom_point(aes(x=x, y=y2, colour=name_y2))
	+scale_colour_discrete(name="Names",
		breaks=c(NULL
		,name_y1
		,name_y2
		)
		, labels=c(NULL
		,name_y1
		,name_y2
		)
	)
)
dev.off()
#------------------------------------------------------------------


name = "Lambda" #lambda ou methode
param_fix = "Methode-3_14_06-08_07" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = name
legend_y_axis = "Score"
ptn_size = 12

x=c(1,0.95,0.9,0.85,0.8,0.75,0.7)
name_y1="CLINTON"
y1=c(1.3765808096891505,1.3765808096891505,1.3765808096891505,1.3765808096891505,1.3765808096891505,1.3765808096891505,1.3765808096891505)
name_y2="TRUMP"
y2=c(0.5980430053973023,0.5980430053973023,0.5980430053973023,0.5980430053973023,0.5980430053973023,0.5980430053973023,0.5980430053973023)
nb_val = length(y1)
size = 0:(nb_val-1)

png(file=paste("Variation_Scores_", name, "_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste("Variation Scores ", name, " ", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=y1, colour=name_y1))
	+geom_point(aes(x=x, y=y1, colour=name_y1))
	+geom_line(aes(x=x, y=y2, colour=name_y2))
	+geom_point(aes(x=x, y=y2, colour=name_y2))
	+scale_colour_discrete(name="Names",
		breaks=c(NULL
		,name_y1
		,name_y2
		)
		, labels=c(NULL
		,name_y1
		,name_y2
		)
	)
)
dev.off()
#------------------------------------------------------------------


name = "Lambda" #lambda ou methode
param_fix = "Methode-4_14_06-08_07" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = name
legend_y_axis = "Score"
ptn_size = 12

x=c(1,0.95,0.9,0.85,0.8,0.75,0.7)
name_y1="CLINTON"
y1=c(33.99999999999998,33.99999999999998,33.99999999999998,33.99999999999998,33.99999999999998,33.99999999999998,33.99999999999998)
name_y2="TRUMP"
y2=c(49.199999999999946,49.199999999999946,49.199999999999946,49.199999999999946,49.199999999999946,49.199999999999946,49.199999999999946)
nb_val = length(y1)
size = 0:(nb_val-1)

png(file=paste("Variation_Scores_", name, "_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste("Variation Scores ", name, " ", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=y1, colour=name_y1))
	+geom_point(aes(x=x, y=y1, colour=name_y1))
	+geom_line(aes(x=x, y=y2, colour=name_y2))
	+geom_point(aes(x=x, y=y2, colour=name_y2))
	+scale_colour_discrete(name="Names",
		breaks=c(NULL
		,name_y1
		,name_y2
		)
		, labels=c(NULL
		,name_y1
		,name_y2
		)
	)
)
dev.off()
#------------------------------------------------------------------


name = "Lambda" #lambda ou methode
param_fix = "Methode-5_14_06-08_07" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = name
legend_y_axis = "Score"
ptn_size = 12

x=c(1,0.95,0.9,0.85,0.8,0.75,0.7)
name_y1="CLINTON"
y1=c(53.0,53.0,53.0,53.0,53.0,53.0,53.0)
name_y2="TRUMP"
y2=c(84.39999999999993,84.39999999999993,84.39999999999993,84.39999999999993,84.39999999999993,84.39999999999993,84.39999999999993)
nb_val = length(y1)
size = 0:(nb_val-1)

png(file=paste("Variation_Scores_", name, "_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste("Variation Scores ", name, " ", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=y1, colour=name_y1))
	+geom_point(aes(x=x, y=y1, colour=name_y1))
	+geom_line(aes(x=x, y=y2, colour=name_y2))
	+geom_point(aes(x=x, y=y2, colour=name_y2))
	+scale_colour_discrete(name="Names",
		breaks=c(NULL
		,name_y1
		,name_y2
		)
		, labels=c(NULL
		,name_y1
		,name_y2
		)
	)
)
dev.off()
#------------------------------------------------------------------


name = "Lambda" #lambda ou methode
param_fix = "Methode-6_14_06-08_08" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = name
legend_y_axis = "Score"
ptn_size = 12

x=c(1,0.95,0.9,0.85,0.8,0.75,0.7)
name_y1="CLINTON"
y1=c(0.6907177610498181,0.6907177610498181,0.6907177610498181,0.6907177610498181,0.6907177610498181,0.6907177610498181,0.6907177610498181)
name_y2="TRUMP"
y2=c(0.42420017575101704,0.42420017575101704,0.42420017575101704,0.42420017575101704,0.42420017575101704,0.42420017575101704,0.42420017575101704)
nb_val = length(y1)
size = 0:(nb_val-1)

png(file=paste("Variation_Scores_", name, "_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste("Variation Scores ", name, " ", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=y1, colour=name_y1))
	+geom_point(aes(x=x, y=y1, colour=name_y1))
	+geom_line(aes(x=x, y=y2, colour=name_y2))
	+geom_point(aes(x=x, y=y2, colour=name_y2))
	+scale_colour_discrete(name="Names",
		breaks=c(NULL
		,name_y1
		,name_y2
		)
		, labels=c(NULL
		,name_y1
		,name_y2
		)
	)
)
dev.off()
#------------------------------------------------------------------


name = "Lambda" #lambda ou methode
param_fix = "Methode-7_14_06-08_08" #parametre fixe avec valeur
background = "white"
size_x = 720
size_y = 480
legend_x_axis = name
legend_y_axis = "Score"
ptn_size = 12

x=c(1,0.95,0.9,0.85,0.8,0.75,0.7)
name_y1="CLINTON"
y1=c(1.3765808096891505,1.3765808096891505,1.3765808096891505,1.3765808096891505,1.3765808096891505,1.3765808096891505,1.3765808096891505)
name_y2="TRUMP"
y2=c(0.5980430053973023,0.5980430053973023,0.5980430053973023,0.5980430053973023,0.5980430053973023,0.5980430053973023,0.5980430053973023)
nb_val = length(y1)
size = 0:(nb_val-1)

png(file=paste("Variation_Scores_", name, "_", param_fix, ".png", sep=""), bg=background, width=size_x, height=size_y, pointsize=ptn_size)
(ggplot(NULL,aes(x=legend_x_axis,y=legend_y_axis))
	+xlab(legend_x_axis)
	+ylab(legend_y_axis)
	+expand_limits(x=c(min(x),max(x)))
	+ggtitle(paste("Variation Scores ", name, " ", param_fix, sep=""))
	+theme(plot.title=element_text(face="bold", hjust=0.5, vjust=0.5))
	+scale_x_continuous(limits = c(min(x), max(x)), breaks = x)
	+geom_line(aes(x=x, y=y1, colour=name_y1))
	+geom_point(aes(x=x, y=y1, colour=name_y1))
	+geom_line(aes(x=x, y=y2, colour=name_y2))
	+geom_point(aes(x=x, y=y2, colour=name_y2))
	+scale_colour_discrete(name="Names",
		breaks=c(NULL
		,name_y1
		,name_y2
		)
		, labels=c(NULL
		,name_y1
		,name_y2
		)
	)
)
dev.off()
#------------------------------------------------------------------


