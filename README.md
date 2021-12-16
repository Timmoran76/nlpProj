# Article Keyword Generation 

## Running Programs with Tags
Baseline models -> python baseline.py
Run base: change arguments in main to be False and False 
Run with pronouns only: change arguments in main to be True and False
Run with title bias only: change arguments in main to be False and True 
Run with pronouns only + title bias: change arguments in main to be True and True 

RAKE model -> python rake1.py

TF-IDF base -> python idf.py
TF-IDF with pronouns only -> python idfP.py

## Running Programs without Tags
If you have your own json file, ensure it is an array of dictionaries that each have an "article" field. The "title" field is also necessary for the baseline models. Then simply append that file name to the aforementioned python commands to run and see what tags each model generates. 
For example: 
python3 baseline.py test.json OR python3 idf.py test.json OR...
