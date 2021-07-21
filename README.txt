Detecting News Tone Using Sentiment Analysis

WORKFLOW: 

Scrape the articles and headings for The Guardian Media Group/The Telegraph/The Independent ->
Parse saved articles in the .json format and process the text ->
Perform sentiment analysis on each set of data, store results in .csv files

The following steps will allow you to run the set of scripts that make up this research project on any Linux distribution.

1) While we have ensured that the latest version of Python will be installed prior to running the scripts so there are no compatibility errors, you might have an older version of Python pre-installed and set as the default on your system. To make sure, please check using 'python --version' and set the version to 3.6.9 if an older one is detected. 

2) Please ensure that 'venv' is installed on your Linux distribution, as all execution will be performed in a virtual environment that the setup script will create automatically. To check, type 'sudo apt-get install python3-venv' into the terminal. 

3) Extract the .zip file provided (here: https://drive.google.com/file/d/1uNJ-AUe2WSx5wRRXOLOI0A_dKRyr3nVq/view?usp=sharing, in case you are unable to access the files here) to the location where you want to run the project. Run the setup file using 'bash setup.sh' in the terminal after navigating to the directory where you extracted the .zip file. The shell script will perform the rest of the process automatically. Please be patient as this will scrape and store over a thousand articles sourced from multiple publications, it might take over half an hour to accomplish this. 

4) You can use the .R scripts provided in the results folders for each media group to visualize the results, or check the graphs provided for an idea of what the results mean. You can also modify the code to work with the new .csv files the setup will generate following sentiment analysis.

                                                   *               *                *
