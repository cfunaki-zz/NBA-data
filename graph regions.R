library(ggplot2)
library(RColorBrewer)

path <- "C:/Users/Chris/Documents/Shot charts/NBA data project/processed_shots/shots_regions_2015.csv"
shots <- read.csv(path, header = F)
names(shots) <- c("player", "team", "x", "y", "made", "three", "period", "minutes", "xbox", "ybox", "region")

team