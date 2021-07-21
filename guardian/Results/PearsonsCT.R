# program to calculate Pearson's Correlation Test for The Guardian/The Guardian Weekly/The Observer

library(ggplot2)
library(dplyr)

# loading the data from the .csv file
df <- read.csv("guardian_headings.csv",
               header = TRUE,
               quote = "\"",
               stringsAsFactors = TRUE,
               strip.white = TRUE)

# Getting the sentiment scores of heading and body as vectors 
heading_sentiment <- dplyr::pull(df, head_score)
body_sentiment <- dplyr::pull(df, body_score)
head_emotion <- dplyr::pull(df, sntmnt)
body_emotion <- dplyr::pull(df, sntmnt2)

# Storing differences in the sentiments of body/heading for each article as 
# another vector 
differences <- heading_sentiment - body_sentiment

# Converting the vector of differences to data-frame for further analysis
sent_diff <- data.frame(differences)

# Creating a data frame of just heading/body sentiment scores
scores_h <- data.frame(heading_sentiment, head_emotion)
scores_b <- data.frame(body_sentiment, body_emotion)

# Plotting a density plot
ggplot(scores_h, aes(x=heading_sentiment, color=head_emotion)) +
  geom_density()
# Adding mean lines
p<-ggplot(scores_h, aes(x=heading_sentiment, color=head_emotion)) +
  geom_density()

ggplot(scores_b, aes(x=body_sentiment, color=body_emotion)) +
  geom_density()
# Adding mean lines
p<-ggplot(scores_b, aes(x=body_sentiment, color=body_emotion)) +
  geom_density()


# Finding four cluster centers
cluster <- kmeans(sent_diff$differences, centers = 4)

# Extracting cluster centers vector
cluster.centers <- as.factor(round(fitted(cluster, method=c("centers", "classes"))))

# Visualizing the clusters
ggplot(sent_diff, aes(x=differences, y=differences)) +    # Below we color by cluster.centers vector
  geom_point()

# Plotting an elbow diagram to check the optimal number of clusters
wss <- sum(kmeans(sent_diff,centers=1)$withinss)
itermax <- min(length(unique(sort(sent_diff$differences))),573)
for (i in 2:itermax) wss[i] <- sum(kmeans(sent_diff,centers=i)$withinss)

plot(1:itermax,wss, type="b", xlab="Number of Clusters",ylab="Within groups sum of squares")
points(1:itermax,wss,pch=16,col="red")

# Finally, performing the Pearson's Correlation Test and checking for positive correlation
res <- cor.test(df$head_score, df$body_score, 
                method = "pearson")
res
