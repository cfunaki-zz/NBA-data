library(ggplot2)


circleFun <- function(center = c(0,0),diameter = 1, npoints = 100){
  r = diameter / 2
  tt <- seq(0,2*pi,length.out = npoints)
  xx <- center[1] + r * cos(tt)
  yy <- center[2] + r * sin(tt)
  return(data.frame(x = xx, y = yy))
}

#outside box
leftline <- data.frame(x = c(-250,-250),y=c(-47.5,302.5))
baseline <- data.frame(x = c(-250, 250),y=c(-47.5,-47.5))
rightline <- data.frame(x = c(250,250),y=c(-47.5,302.5))
#solid FT semicircle
ft_top_circle <- data.frame(x=c(-60000:0/1000,0:60000/1000),y=c(-280+sqrt(60^2-c(-60000:0/1000,0:60000/1000)^2)))
#lower FT semicircle
ft_circle <- circleFun(c(0, 142.5), 120, npoints=100)
#key
key <- data.frame(x=c(-80,-80,80,80,-80),y=c(-47.5,142.5,142.5,-47.5,-47.5))
#box inside the key
box_in_key <- data.frame(x = c(-60,-60,60,60,-60), y = c(-47.5,142.5,142.5,-47.5,-47.5))
# restricted area semicircle
restricted_area <- data.frame(x=c(-470000:0/1000,0:40000/1000),
                              y=c(sqrt(40^2-c(-470000:0/1000,0:40000/1000)^2)))
#rim
rim <- circleFun(c(0, 0), 15, npoints = 100)
#backboard
backboard <- data.frame(x = c(-30,30), y = c(-12.5,-12.5))
#three point line
three_arc <- data.frame(x=c(-220,-220,-220000:0/1000,0:220000/1000,220,220),
                        y=c(-47.5,1690/120-47.5,sqrt(237.5^2-c(-220000:0/1000,0:220000/1000)^2),1690/120-47.5,-47.5))



player1 <- "Stephen Curry"
player2 <- "Dwight Howard"

# Player boxes
path1 <- "C:/Users/Chris/Documents/Shot charts/NBA data project/player_processed"
file1 <- paste(player1, 'processed.csv', sep='_')
player_boxes <- read.csv(file.path(path1, file1), header = T)
player_boxes$made <- as.factor(player_boxes$made)

# player 1 individual
path2 <- "C:/Users/Chris/Documents/Shot charts/NBA data project/player_shots_2015"
file2 <- paste(player1, 'shots.csv', sep='_')
player1_shots <- read.csv(file.path(path2, file2), header = F)
names(player1_shots) <- c("player", "team", "x", "y", "made", "three", "period", "minutes")
player1_shots$made <- as.factor(player1_shots$made)

# player 2 individual
path2 <- "C:/Users/Chris/Documents/Shot charts/NBA data project/player_shots_2015"
file2 <- paste(player2, 'shots.csv', sep='_')
player2_shots <- read.csv(file.path(path2, file2), header = F)
names(player2_shots) <- c("player", "team", "x", "y", "made", "three", "period", "minutes")
player2_shots$made <- as.factor(player2_shots$made)

player_shots <- rbind(player1_shots, player2_shots)


width = 1.1
col1 = 'gray90' # light gray
col2 = 'gray18' # dark gray
scatter_players <- ggplot() + 
  #geom_tile(data=player_boxes, aes(x, y, fill = fitted)) + 
  geom_point(data=player_shots, mapping=aes(x, y, color=player)) +
  #geom_point(data=player_boxes, mapping=aes(x, y, colour=sse, size=log(taken))) +
  
  geom_line(data=leftline, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=baseline, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=rightline, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=ft_circle, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=key, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=box_in_key, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=restricted_area, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=rim, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=backboard, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=three_arc, aes(x,y), fill=NA, color=col1, lwd=width) +
  scale_x_continuous(limits = c(-250, 250)) +
  scale_y_continuous(limits = c(-47.5, 302.5)) +
  scale_colour_manual(values = c("steelblue1","firebrick1")) +

  coord_fixed() +
  guides(colour = guide_legend(override.aes = list(size=4))) +
  theme(panel.background = element_rect(fill = col2),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.line = element_blank(), 
        axis.text.x = element_blank(), 
        axis.text.y = element_blank(),
        axis.ticks = element_blank(), 
        axis.title.x = element_blank(), 
        axis.title.y = element_blank(),
        legend.position = c(0.15, 0.90),
        legend.title = element_blank(),
        legend.background = element_blank(),
        legend.key = element_blank(),
        legend.text = element_text(colour=col1, size=16, face='bold'))
scatter_players


#ggsave(filename = 'C:/Users/Chris/Documents/Shot charts/NBA data project/charts/steph_dwight.png',
#       plot = scatter_players,
#       dpi = 120)