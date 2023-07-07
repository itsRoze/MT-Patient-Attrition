
# RO1 Prediction Algorithm

This set of python scripts can read data from the R01 Datbase of MindTrails and make predictions about the likelyhood of 
dropout prior to completing the study.

More inteligent people could speak to all its beauty comlexity and raw machine intelligence, but as usual
it falls on the more dim witted of us to write the darn readme files.

# Important Files
1. **VERSION**:  This should be updated whenever committing new code to the repository.  It can help us
identify the version of this algorithm that is used to make a prediction.  I can be anything, but should
be short (<255 char) and somewhat descriptive.  This will be included in the database beside each 
prediction that is made.
2. **creds.secret** There is an example file.  This contains all the data you need to connect to the mysql
database.  Copy the example to creds.secret, and fix it so it says all the right stuff.  The actual file
is git ignored, so you don't have to worry about comitting your secrets, or getting your secrets overwritten
by the secrets of some poor fool that commtted theirs.

# Dependencies
* Dependencies are listed in the requirements.txt file.  If you don't use a virtual environment, start.  Use this to 
install all the dependencies. [VirtualEnv](https://virtualenv.pypa.io/en/latest/installation/) is your best and most 
precious python friend.  With it installed, and a new VENV activated, just
```commandline
pip install -r requirements.txt
```

# Testing 1 participant
With at least one fully populated record in the R01 database, execute:
```commandline
python R01_dropout_prediction.py
```

More details will come.




