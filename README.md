
### Virtual Environment
pip install virtualenv
virtualenv --version
python3.10 -m venv venv
 -- or --
virtualenv <env-name>
source <env-name>/bin/activate
deactivate


# RUN ENVIRONMENT

/desktop/code/leadgen/grok.sh
/desktop/code/leadgen/gpt_spacy/run.sh
/desktop/code/leadgen/gpt-reception/run.sh
/desktop/code/leadgen/gpt-phone/run.sh


### heroku and flask
Maks sure Procfile is there and it is correct.
Add gunicorn with pip and freeze it to requirements.txt


### create a requirement file
pip3 freeze > requirements.txt
pip3 install -r requirements.txt


### unit test entire directory.
python -m unittest discover -s <directory_name>
### run all unit test
python -m unittest discover -v
### unit test debug
python -m unittest <test_file> --pdb


## merge dev to main (production)
git checkout main
git pull
git merge dev
git push
git checkout dev



## PACKAGE

## create a setup.py file

## compile for package
python setup.py sdist

## pip install which allows debugging.
pip install -e ../../gpt_redis



# Creating Source Distributions:
python setup.py sdist
# Creating Wheel Distributions:
pip install wheel
python setup.py bdist_wheel
# Develop Mode
python setup.py develop
# Clean build artifact
python setup.py clean --all
