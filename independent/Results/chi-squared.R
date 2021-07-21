# Program to perform chi-squared test

# Read in the .csv file
df <- read.csv("independent_final.csv",
               header = TRUE,
               quote = "\"",
               stringsAsFactors = TRUE,
               strip.white = TRUE)

# Create a table from the columns with sentiments of heading and article
tbl <- table(df$sntmnt, df$sntmnt3)

# Print the table to check if the above operation was performed successfully 
tbl

# Conduct chi-squared test 
chisq.test(tbl) 
