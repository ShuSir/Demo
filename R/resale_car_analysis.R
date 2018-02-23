# Analysis of Car Resale Market 
# 
# This dataset was collected from car sale advertisements for study/practice purposes in 2016. This dataset contains data for more than 9.5K cars sale in Ukraine. Most of them are used cars so it opens the possibility to analyze features related to car operation. 
# source: https://www.kaggle.com/antfarol/insights-from-cars-sale-ads/data
# 
# Dataset contains 9576 rows and 10 variables with essential meanings:
# 
# car: manufacturer brand
# price: seller’s price in advertisement (in USD)
# body: car body type
# mileage: as mentioned in advertisement (‘000 Km)
# engV: rounded engine volume (‘000 cubic cm)
# engType: type of fuel (“Other” in this case should be treated as NA)
# registration: whether car registered in Ukraine or not
# year: year of production
# model: specific model name
# drive: drive type

{r eval=FALSE} 
library(tidyverse)
library(corrplot)

{r echo=FALSE} 
raw=read.csv(file="/Users/ShuSir/Desktop/Sublime/Dashboard/data/car_ad.csv", header = TRUE)

raw$age=as.numeric(format(Sys.Date(),'%Y'))-raw$year
colnames(raw)
raw$category=paste(raw$car,raw$model)
data=raw[c("car","price","body",'mileage','engV','engType','age','model','drive','category')]

# What's the most popular car on the second-hand car market ? --- Mercedes-Benz E-class

rank=data %>% group_by(category)%>%summarise(carNum=n(),medianMile=round(median(mileage),1),medianAge=round(mean(age),1))%>% arrange(desc(carNum))%>%as.data.frame()

head(rank, 20)

# Does short age always corresond to short mileage? Not really. Results shows that some very old car has relatively smaller mileage, fishy.Yet some very young car (and buyer may feel the car is newer) has large mileage. 

group= data %>% group_by(age) %>% 
  summarise(carNum = n(), medianRun = median(mileage))

ggplot(group, aes(x = age, y = medianRun)) + geom_line(colour = "#66CC99") +
  scale_x_continuous(breaks=seq(0, 50, 5), limits= c(0, 50)) +
  ggtitle("Median Mileage vs. Car Age")

# an overview of the correlation of different arribute
attribute=raw[c("price","body",'mileage','engType','age','model','drive','car')]
attribute$price=as.numeric(attribute$price)
attribute$body=as.numeric(attribute$body)
attribute$mileage=as.numeric(attribute$mileage)
attribute$engType=as.numeric(attribute$engType)
attribute$model=as.numeric(attribute$model)
attribute$drive=as.numeric(attribute$drive)
attribute$car=as.numeric(attribute$car)

correlations=cor(attribute)
correlations[, !colSums(is.na(correlations)) >1,drop=FALSE]

corrplot(correlations,method="circle")
