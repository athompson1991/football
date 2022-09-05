# Fantasy Football Predictor

The draft was approaching. I knew web scraping and how to
do machine learning regressions using scikit-learn. It seemed
only natural to try and game out my picks in one way or another.

I scrape the website https://www.pro-football-reference.com/ for this project.

There's a massive tutorial to explain all this that I wrote located here: 

http://www.kingzephyr.com/2019/09/13/fantasy-football-with-scrapy-and-scikit-learn-part-1/

http://www.kingzephyr.com/2019/09/13/fantasy-football-with-scrapy-and-scikit-learn-part-2/

### Prerequisites

I am assuming Python 3 is installed on the system, as well as Git.  

### To run the code


__TLDR__: Assuming everything works as expected, the full script _should_ be

```
cd ~
mkdir project
cd project

python -m venv football_venv
source football_venv/bin/activate

git clone https://github.com/athompson1991/football.git
cd football

pip install -r requirements.txt

mkdir script/data

scrapy crawl passing
scrapy crawl receiving
scrapy crawl defense
scrapy crawl kicking

cd script
python run_script.py
```

##### Step-by-Step

Navigate to an empty directory.

```
cd ~
mkdir project
cd project
```

Now make your Python environment and activate said environment.

```
python -m venv football_venv
source football_venv/bin/activate
```

Clone this repo to your local machine, then `cd` into the directory

```
git clone https://github.com/athompson1991/football.git
cd football
```

Install requirements

```
pip install -r requirements.txt
```


Now for the fun part. The project requires a directory to store the data, 
so make the directory in the proper location

```
mkdir script/data
```


Scrape all the data

```
scrapy crawl passing
scrapy crawl receiving
scrapy crawl passing
```

This scrapes the website and saves our "database" as `csv` files to the directory we just made.

Now simply run the script to crunch all the numbers

```
cd script
python run_script.py
```

That should do it! Once the script runs all the way through,
there should be a `power_rankings.csv` file in your `script/data` directory.
This means that the script successfully fit and tuned 21 regression models,
then used those models to produce a power ranking.
