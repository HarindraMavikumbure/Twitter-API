# Twitter-API
Uses the twitter API to extract tweets given search queries set in config.ini
## Installation instructions 

To install the required libraries:

  #### pip install -r requirements.txt
  
This code was developed to be run from within colab. 
This direct link will open a copy of "run_in_colab.ipynb" within colab
https://colab.research.google.com/github/HarindraMavikumbure/Twitter-API/blob/main/run_in_colab.ipynb


## Usage instructions 
Run the first cell within colab (!git clone). This will clone the github project into colab's /content/ folder. 
The config file now resides at: 

/content/Twitter-API/config.ini

This config file contains details pertaining to the program's parameters. By default, it will run a hashtag search, a mention search, and a key phrase search. Editing the parameters of the config file will allow you to add your own API key, omit search types, change search phrases, and change the location of the CSV export directory.   

When the config file is to your liking, run the second cell (!python Twitter-API/main.py). The specified search or searches will run and CSV files will be exported to the folder you specified. 

If you don't see the folder or the CSV files in colab's file system after running the program in your web browser, try hitting the built-in refresh button at the top of colab's file system.
