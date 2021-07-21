# program to find clusters using k-means analysis and plot them

library(ggplot2)
library(dplyr)
library(fpc)

# read in the data
df <- read.csv("independent_final.csv",
               header = TRUE,
               quote = "\"",
               stringsAsFactors = TRUE,
               strip.white = TRUE)

# Getting the sentiment scores of heading and body as vectors 
heading_sentiment <- dplyr::pull(df, sentiment_score)
body_sentiment <- dplyr::pull(df, sentiment_score2)
head_emotion <- dplyr::pull(df, sntmnt)
body_emotion <- dplyr::pull(df, sntmnt2)

# Storing differences in the sentiments of body/heading for each article as 
# another vector 
differences <- heading_sentiment - body_sentiment

# Convert the vector of differences to data-frame for further analysis

sent_diff <- data.frame(differences)


# Find five cluster centers

mymeans <- kmeans(sent_diff$differences, centers = 5)

# Centroid Plot against 1st 2 discriminant functions
plotcluster(sent_diff$differences, mymeans$cluster)

