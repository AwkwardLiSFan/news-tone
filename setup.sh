#!/bin/bash
sudo apt-get install python3
#virtualenv project -p usr/bin/python3
python3 -m venv project
source project/bin/activate
# virtual environment is now active
# install pip before other dependencies
sudo apt install python3-pip
# now proceed to install remaining dependencies for the project
pip3 install -r requirements.txt

# load required NLTK packages for the analysis
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader wordnet
python3 -m nltk.downloader sentiwordnet
python3 -m nltk.downloader punkt
python3 -m nltk.downloader averaged_perceptron_tagger

# now we start running the main programs. Let's start with The Guardian Media Group

# get the news articles from The Guardian, The Guardian Weekly and The Observer
python3 guardian/main.py
# now carry out sentiment analysis for all three
python3 guardian/process_text.py

# now carry out sentiment analysis for The Daily Telegraph and The Sunday Telegraph
python3 telegraph/main.py
# now carry out sentiment analysis for both of the above
python3 telegraph/process_text.py

# now carry out sentiment analysis for The Independent
python3 independent/main.py
# now carry out sentiment analysis for both of the above
python3 independent/process_text.py

