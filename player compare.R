library(dplyr)
library(ggplot2)
library(mgcv)

# NBA league data
path_league <- "E:/NBA data project/processed_shots"
shots_raw <- read.csv(file.path(path_league, "shots_clean_2014.csv"), header = F)
names(shots_raw) <- c("player", "team", "x", "y", "made", "three", "period", "minutes")

shots_raw <- shots_raw %>%
  mutate(r = sqrt(x^2 + y^2),
         theta = ifelse(x >= 0, -atan(y/x) + pi / 2, -atan(y/x) - pi / 2))

ggplot(shots_raw, aes(theta, r, color = made)) + 
  geom_point()


# Lebron data
path_player <- "E:/NBA data project/player_shots"
player_shots <- read.csv(file.path(path_player, "Stephen Curry_shots.csv"), header = F)
names(player_shots) <- c("player", "team", "x", "y", "made", "three", "period", "minutes")

player_shots <- player_shots %>%
  mutate(r = sqrt(x^2 + y^2),
         theta = ifelse(x >= 0, -atan(y/x) + pi / 2, -atan(y/x) - pi / 2))

ggplot(player_shots, aes(theta, r, color = made)) + 
  geom_point()

# GAM
# Model NBA
league_model <- gam(made ~ s(theta, r), family = binomial(link = "logit"), data = shots_raw)
plot(league_model)

league.grid <- expand.grid(x = with(shots_raw, seq(-245, 245, length.out = 50)), 
                    y = with(shots_raw, seq(-47.5, 302.5, length.out = 36))) %>% 
  mutate(r = sqrt(x^2 + y^2),
         theta = ifelse(x >= 0, -atan(y/x) + pi / 2, -atan(y/x) - pi / 2))

fitted <- predict(league_model, newdata = league.grid, type = "response")
league.grid$fitted <- fitted

ggplot(league.grid, aes(x, y, fill = fitted)) + 
  geom_tile() + 
  stat_contour(aes(z = fitted), binwidth = 0.025) +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0.3,
                       space = "Lab", na.value = "grey50", guide = "colourbar")


# Model Lebron
player_model <- gam(made ~ s(theta, r), family = binomial(link = "logit"), data = player_shots)
plot(player_model)

player.grid <- expand.grid(x = with(player_shots, seq(-245, 245, length.out = 50)), 
                           y = with(player_shots, seq(-47.5, 302.5, length.out = 36))) %>% 
  mutate(r = sqrt(x^2 + y^2),
         theta = ifelse(x >= 0, -atan(y/x) + pi / 2, -atan(y/x) - pi / 2))

fitted <- predict(player_model, newdata = player.grid, type = "response")
player.grid$fitted <- fitted

ggplot(player.grid, aes(x, y, fill = fitted)) + 
  geom_tile() + 
  stat_contour(aes(z = fitted), binwidth = 0.025)

stats$player_fitted <- player.grid$fitted

player.grid$diff <- player.grid$fitted - league.grid$fitted

ggplot(player.grid, aes(x, y, fill = diff)) +
  geom_tile() +
  stat_contour(aes(z = fitted), binwidth = 0.025) +
  scale_fill_gradient2(low = "blue", mid="white", high = "red", space = "Lab", na.value = "grey50", guide = "colourbar")


predict(player_model, newdata = data.frame(r=5, theta=1.1), type= "response")
