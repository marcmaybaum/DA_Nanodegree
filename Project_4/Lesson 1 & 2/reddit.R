getwd()
setwd('~/Downloads')

reddit <- read.csv('reddit.csv')
summary(reddit)
table(reddit$employment.status)

row.names(reddit)

# str lets you look at variables and types of data
str(reddit)

# levels lets us know the multiple values for a column
levels(reddit$age.range)

library(ggplot2)
qplot(data = reddit, x =age.range, order = asc)

# Two ways to order the range of Age & Salary correctly in plot
# See below for examples

# Using ordered() function
reddit$age.range <- ordered(reddit$age.range, levels = c("Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or Above"))
qplot(data=reddit, x=age.range)

# Using factor() function
reddit$age.range <- factor(reddit$age.range, levels = c("Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or Above"), ordered = T)
qplot(data=reddit, x=age.range)

