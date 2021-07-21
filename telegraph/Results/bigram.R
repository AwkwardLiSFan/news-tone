# program to explore bigrams in the collected data

library(ggplot2)
library(dplyr)
library(tidytext)
library(tidyr)

# read in the data from the .csv file
df <- read.csv("telegraph_matches.csv",
               header = TRUE,
               quote = "\"",
               stringsAsFactors = TRUE,
               strip.white = TRUE)

# convert it to a dataframe for further operations
h <- data.frame(txt = df$body,stringsAsFactors = FALSE)

# make a preliminary list of negation words
negation_words <- c("not", "no", "never", "without")

# carry out the bigram analysis and find out the most popular words preceded by a negation word
h %>% 
  unnest_tokens(word, txt, token = "ngrams", n = 2) %>% 
  separate(word, c("word1", "word2"), sep = " ") %>%
  filter(word1 %in% negation_words) %>% 
  filter(!word2 %in% stop_words$word) %>% 
  unite(word,word1, word2, sep = " ") %>% 
  count(word, sort = TRUE) %>% 
  slice(1:10)%>%
  ggplot() + geom_bar(aes(word, n), stat = "identity", fill = "#add8e6") +
  theme_minimal() +
  labs(title = "Top Bigrams of Negated Words",
       caption = "Data Source: The Telegraph (Body)")


