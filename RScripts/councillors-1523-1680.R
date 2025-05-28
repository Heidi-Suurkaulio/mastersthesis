library("dplyr")
setwd("~/GraduData/")

#### functions ####
noble_ranks <- function(data) {
  ranks <- gsub("Uradel.*", "Uradel", data$Noble_rank)
  ranks <- gsub("Estate.*", "Estate unknown", ranks)
  ranks <- gsub("Ennoble.*", "Ennobled", ranks)
  ranks <- gsub("Commone.*", "Commoner", ranks)
  return(table(ranks))
}

appointed_by_monarch <- function(year1, year2) {
  filterd <- filter(full_data, between(Appointed, year1, year2))
  return(nrow(filterd))
}

#### handling the original dataset ####
full_data <- read.csv("Councillors_of_the_Realm1523-1680.csv", sep = ";", header = TRUE)

full_actual <- noble_ranks(full_data)
full_actual
full_prop <- prop.table(noble_ranks(full_data))
full_prop

before <- filter(full_data, Appointed < 1523)
nrow(before)
x <- c(appointed_by_monarch(1523, 1560), appointed_by_monarch(1561, 1568),
       appointed_by_monarch(1569, 1592), appointed_by_monarch(1593, 1599),
       appointed_by_monarch(1600, 1611), appointed_by_monarch(1612, 1632),
       appointed_by_monarch(1633, 1643), appointed_by_monarch(1644, 1654),
       appointed_by_monarch(1655, 1660), appointed_by_monarch(1661, 1671),
       appointed_by_monarch(1672, 1697))
x
y <- c("G I", "E XIV", "J III", "Si", "C IX", "G II", "reg", "Ch", "C X", "reg", "C XI")
barplot(x, names.arg = y, xlab = "Monarch", ylab = "Councillors appointed" , col = "black")

#### handling the dataset prior 1600 ####
prior_1600 <- filter(full_data, Appointed <= 1600)
nrow(prior_1600)
prior_1600_actual <- noble_ranks(prior_1600)
prior_1600_actual
prior_1600_prop <- prop.table(noble_ranks(prior_1600))
prior_1600_prop

#### handling the dataset post 1600 ####
post_1600 <- filter(full_data, Appointed >= 1601)
nrow(post_1600)
post_1600_actual <- noble_ranks(post_1600)
post_1600_actual
post_1600_prop <- prop.table(noble_ranks(post_1600))
post_1600_prop

### handling the dataset during the reign of Christina
reign_of_C <- filter(full_data, between(Appointed, 1644, 1654))

#counting the age distributions of the appointed councillors
summary(reign_of_C$Age)
summary(full_data$Age)

#plotting the age distribution
#plot(density(reign_of_C$Age, na.rm = TRUE))
#plot(density(full_data$Age, na.rm = TRUE))

#filtering the youngest and oldest (see the pattern)
#filter(full_data, Age == 74)
#filter(reign_of_C, Age == 61)
