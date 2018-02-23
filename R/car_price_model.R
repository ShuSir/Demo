## change Lib 
library(utils)
options(repos='http://cran.ma.imperial.ac.uk/')
.libPaths(c("C://Shu//library", .libPaths()))


install.packages("tidyverse")
install.packages("dplyr")
library(tidyverse)
library(devtools)
library(dplyr)
library(magrittr)

data=read.csv(file="F:/BBGWS/Git/codestuff/dashboard/data/car_ad.csv", header = TRUE)
str(data )
rank=data%>%summary(carNum=n(),medianCost=round(median(price),1),meanCost=round(mean(price),1))%>%as.data.frame()

runByAge <- df %>%  
  group_by(age) %>% 
  summarise(carNum = n(), medianRun = median(annualRun), meanRun = mean(annualRun))
