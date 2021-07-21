# program to plot an elbow diagram and density plots using k-means analysis

library(ggplot2)
library(dplyr)

df <- read.csv("telegraph_matches.csv",
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

# Creating a data frame of just heading/body sentiment scores
scores_h <- data.frame(heading_sentiment, head_emotion)
scores_b <- data.frame(body_sentiment, body_emotion)

# Plotting a density plot
ggplot(scores_h, aes(x=heading_sentiment, color=head_emotion)) +
  geom_density()
# Add mean lines
p<-ggplot(scores_h, aes(x=heading_sentiment, color=head_emotion)) +
  geom_density()

ggplot(scores_b, aes(x=body_sentiment, color=body_emotion)) +
  geom_density()
# Add mean lines
p<-ggplot(scores_b, aes(x=body_sentiment, color=body_emotion)) +
  geom_density()


# Using 5 clusters initially
cluster <- kmeans(sent_diff$differences, centers = 5)

cluster.centers <- as.factor(round(fitted(cluster, method=c("centers", "classes"))))

# Plotting the clusters' densities
ggplot(sent_diff, aes(x=differences)) +    # Below we color by cluster.centers vector
  geom_density(aes(group=cluster.centers, color=cluster.centers, fill=cluster.centers), alpha=0.3) +
  labs(title = "Density Plot of Clusters")

# plotting an elbow diagram to find optimum number of clusters
wss <- sum(kmeans(sent_diff,centers=1)$withinss)
itermax <- min(length(unique(sort(sent_diff$differences))),778)
for (i in 2:itermax) wss[i] <- sum(kmeans(sent_diff,centers=i)$withinss)

# Spotting the bend in the elbow diagram
plot(1:itermax,wss, type="b", xlab="Number of Clusters",ylab="Within groups sum of squares")
points(1:itermax,wss,pch=16,col="red")
