# program to plot a scatterplot and look for a hint of relation b/w heading and body sentiment

library(ggplot2)
library(dplyr)
library(car)

# Loading the data from a .csv file
df <- read.csv("guardian_headings.csv",
               header = TRUE,
               quote = "\"",
               stringsAsFactors = TRUE,
               strip.white = TRUE)

# Getting the sentiment scores of heading and body as vectors 
heading_sentiment <- dplyr::pull(df, head_score)
body_sentiment <- dplyr::pull(df, body_score)

# Creating a data frame of just heading/body sentiment scores
scores <- data.frame(heading_sentiment, body_sentiment)

# Full Scatterplot
scatterplot( body_sentiment ~ heading_sentiment,
             data = scores)

# Positive Body only
scatterplot( body_sentiment>0 ~ heading_sentiment,
             data = scores)
