library(ggplot2)
library(RColorBrewer)
library(plyr)
library(dplyr)

# Player data
player <- "Dwight Howard"

path1 <- "C:/Users/Chris/Documents/Shot charts/NBA data project/player_processed"
file1 <- paste(player, 'processed.csv', sep='_')
player.stats <- read.csv(file.path(path1, file1), header = T)

player.stats$POE_per_shot <- (player.stats$pts - player.stats$exp_pts) / player.stats$taken
#player.stats <- subset(player.stats, !is.na(fg))
player.stats$shots <- player.stats$taken
player.stats$taken <- NULL
player.stats$sse <- NULL


# Player data for modeling
path2 <- "E:/NBA data project/player_shots_2014"
file2 <- paste(player, 'shots.csv', sep='_')
player_shots <- read.csv(file.path(path2, file2), header = F)
names(player_shots) <- c("player", "team", "x", "y", "made", "three", "period", "minutes")

player_shots <- player_shots %>%
  mutate(r = sqrt(x^2 + y^2),
         theta = ifelse(x >= 0, -atan(y/x) + pi / 2, -atan(y/x) - pi / 2))

# Model Player
player_model <- gam(made ~ s(theta, r), family = binomial(link = "logit"), data = player_shots)
plot(player_model)

player.grid <- expand.grid(x = with(player_shots, seq(-245, 245, length.out = 50)), 
                           y = with(player_shots, seq(-47.5, 302.5, length.out = 36))) %>% 
  mutate(r = sqrt(x^2 + y^2),
         theta = ifelse(x >= 0, -atan(y/x) + pi / 2, -atan(y/x) - pi / 2))

player.stats$player_fitted <- predict(player_model, newdata = player.grid, type = "response")

player.stats$POE_per_shot <- player.stats$player_fitted - player.stats$fitted


# Set color limits for graph
lowcol <- -0.15
highcol <- 0.15
player.stats$POE_per_shot[player.stats$POE_per_shot < lowcol] <- lowcol
player.stats$POE_per_shot[player.stats$POE_per_shot > highcol] <- highcol

myPalette <- colorRampPalette(rev(brewer.pal(7, "RdBu")))


# Plot dots
width = 1.1
col1 = 'gray90'
col2 = 'gray18'
player_poe <- ggplot(data=player.stats, aes(x, y, colour = POE_per_shot, size = log(shots))) +
  geom_point() +
  
  geom_line(data=leftline, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=baseline, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=rightline, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=ft_circle, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=key, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=box_in_key, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=restricted_area, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_polygon(data=rim, aes(x,y), fill=NA, color=col1, lwd=1.2) +
  geom_polygon(data=backboard, aes(x,y), fill=NA, color=col1, lwd=width) +
  geom_line(data=three_arc, aes(x,y), fill=NA, color=col1, lwd=width) +
  scale_x_continuous(limits = c(-250, 250)) +
  scale_y_continuous(limits = c(-47.5, 302.5)) +
  scale_size_continuous(range = c(2,5)) +
  coord_fixed() +
  scale_color_gradientn(colours = myPalette(20), limits=c(lowcol, highcol),
                        breaks=c(-0.15,0.5,0.15),labels=c(-0.15,0,0.15)) +
  ggtitle(player) +
  theme(plot.title = element_text(colour=col1, vjust = -3.5, size=24, face='bold')) +
  theme(panel.background = element_rect(fill = col2),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.line = element_blank(), 
        axis.text.x = element_blank(), 
        axis.text.y = element_blank(),
        axis.ticks = element_blank(), 
        axis.title.x = element_blank(), 
        axis.title.y = element_blank(),
        legend.position = "bottom",
        legend.box = "horizontal")
player_poe


path_name <- "E:/NBA data project/charts"
chart_name <- paste(player, 'POE.png', sep='_')
ggsave(filename = chart_name,
       path = path_name,
       plot = player_poe,
       dpi = 120)
