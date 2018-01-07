ggplot(aes(x= price, y=x), data = diamonds) +
  geom_point()

?cor.test()

cor.test(x=diamonds$price, y=diamonds$x)
cor.test(x=diamonds$price, y=diamonds$y)
cor.test(x=diamonds$price, y=diamonds$z)

summary(diamonds)

# Quiz 5
ggplot(aes(x= price, y=depth), data = diamonds) +
  geom_point()

?scale_x_continuous

# Quiz 6
ggplot(data = diamonds, aes(x = depth, y = price)) + 
  geom_point(alpha = 1/100) + 
  scale_x_continuous(breaks= c(0, 80, 2))

summary(diamonds$depth)

# Quiz 7
cor.test(x=diamonds$depth, y=diamonds$price)

# Quiz 8
ggplot(aes(x = price, y = carat), data = diamonds) +
  xlim(0, quantile(diamonds$price, 0.99)) +
  geom_point()

summary(diamonds)
?xlim()

# Quiz 9

diamonds$volume <- diamonds$x * diamonds$y * diamonds$z

ggplot(aes(x = price , y = volume), data = diamonds) +
  geom_point()

# Quiz 11

diamonds_volume <- subset(diamonds, volume != 0 & volume < 800) 

cor.test(x = diamonds_volume$price, y = diamonds_volume$volume)

# Quiz 12

ggplot(aes(x = price , y = volume), data = diamonds_volume) +
  geom_point() + geom_smooth()

# Quiz 13

?dplyr

library('dplyr')

diamondsByClarity <- summarise(diamonds,
                               mean_price = mean(diamonds$price),
                               median_price = median(diamonds$price),
                               min_price = min(diamonds$price),
                               max_price = max(diamonds$price),
                               n = n())

diamondsByClarity <- diamonds %>%
  summarise(mean_price = mean(diamonds$price),
            median_price = median(diamonds$price),
            min_price = min(diamonds$price),
            max_price = max(diamonds$price),
            n = n())

# Quiz 14

library(gridExtra)



# Quiz 16



