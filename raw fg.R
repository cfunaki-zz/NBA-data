library(ggplot2)
library(RColorBrewer)
library(colorspace)

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


# Raw boxes for raw
path2 <- "G:/NBA data project/processed_shots"
file2 <- "raw_boxes_2014.csv"
raw_boxes <- read.csv(file.path(path2, file2), header = F)
names(raw_boxes) <- c('x','y','made','taken','fg','three')
raw_boxes$fg[raw_boxes$taken == 0] <- NA
raw_boxes <- subset(raw_boxes, !is.na(fg))
lowcol <- 0.2
highcol <- 0.6
raw_boxes$fg[raw_boxes$fg < lowcol] <- lowcol
raw_boxes$fg[raw_boxes$fg > highcol] <- highcol
raw_boxes$FGP <- raw_boxes$fg

myPalette <- colorRampPalette(rev(brewer.pal(7, "BrBG")))


# Plot tiles
width = 1.4
col1 = 'gray18'
col2 = 'gray18'
raw_fg <- ggplot(data=raw_boxes, aes(x, y)) +
  geom_tile(aes(fill = FGP), colour = col1) +
  #geom_point(shape = 15, fill = fitted, size = 4) +
  
  geom_line(data=leftline, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=baseline, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=rightline, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=ft_circle, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=key, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=box_in_key, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=restricted_area, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=rim, aes(x,y), fill=NA, color=col1, lwd=1.4) +
  geom_polygon(data=backboard, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=three_arc, aes(x,y), fill=NA, color=col1, lwd=width) +
  scale_x_continuous(limits = c(-250, 250)) +
  scale_y_continuous(limits = c(-47.5, 302.5)) +
  coord_fixed() +
  #scale_fill_manual(values = colorRampPalette(c("#3288bd","#99d594","#e6f598",
  #                                              "#ffffbf","#fee08b", "#fc8d59", "#d53e4f"))(7)) +
  scale_fill_gradientn(colours = myPalette(20), limits=c(lowcol, highcol)) +
  
  theme(#panel.background = element_rect(fill = col2),
        panel.background = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.line = element_blank(), 
        axis.text.x = element_blank(), 
        axis.text.y = element_blank(),
        axis.ticks = element_blank(), 
        axis.title.x = element_blank(), 
        axis.title.y = element_blank(),
        legend.title = element_text(size=16),
        legend.position = "right")
raw_fg

ggsave(filename = 'G:/NBA data project/charts/raw_fg.png',
       plot = raw_fg,
       dpi = 120)
