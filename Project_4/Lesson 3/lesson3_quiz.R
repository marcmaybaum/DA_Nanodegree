### 1st Quiz
library(ggplot2)
data(diamonds)

summary(diamonds)

?diamonds

### 2nd Quiz
ggplot(data=diamonds, aes(x=price)) + 
  geom_histogram(binwidth = 500)

### 3rd Quiz
summary(diamonds$price)

### 4th Quiz
sum(diamonds$price < 500)

sum(diamonds$price < 250)

sum(diamonds$price >= 15000)

### 5th Quiz
ggplot(data=diamonds, aes(x=price)) + 
  geom_histogram(binwidth = 500)

qplot(x = price, data = diamonds, binwidth = 10) +
  scale_x_continuous(limits = c(250,1000))

ggsave('priceHistogram.png')

### 6th Quiz

qplot(x = price, data = diamonds, binwidth = 10) +
  scale_x_continuous(limits = c(250,1000)) +
  facet_wrap(~cut)

### 7th Quiz

by(diamonds$price, diamonds$cut, summary)

### 8th Quiz

qplot(x = price, data = diamonds) + 
  facet_wrap(~cut, scales = "free_y")

?facet_wrap

### 9th Quiz

qplot(x = log(price/carat), data = diamonds) + 
  facet_wrap(~cut, scales = "free_y")

### 10th Quiz

qplot(x = cut, y = price, data = diamonds, geom = 'boxplot')
#  scale_y_continuous(limits = c(0,1000))

qplot(x = gender, y = friend_count,
      data = subset(pf, !is.na(gender)), geom = 'boxplot') +
  coord_cartesian(ylim = c(0,1000))

### 11th Quiz

qplot(x = color, y = price, data = diamonds, geom = 'boxplot')

by(diamonds$price, diamonds$color, summary)

IQR(subset(diamonds, color == 'D')$price)

IQR(subset(diamonds, color == 'J')$price)

### 12th Quiz

qplot(x = carat, y = price, data = diamonds, geom = 'boxplot') +
  facet_wrap(~color)

### 13th Quiz

qplot(x = carat, data = diamonds, geom = 'freqpoly', binwidth = 0.1)

summary(diamonds$carat)

table(diamonds$carat)

### 14th Quiz

# Data munging or data wrangling can take up 
# much of a data scientist's or data analyst's time. 
# There are two R packages that make these tasks 
# easier in R: tidyr and dplyr.

# tidyr -a package that reshapes the layout of your data

# dplyr - a package that helps you transform tidy, tabular data

### 15th Quiz








### 16th Quiz





