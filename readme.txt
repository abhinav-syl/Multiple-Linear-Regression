The model is created using sklearn, a mulitple linear regression model.

A screenshot of sample json data is stored in modules/data

The following approaches were tried:

1. Filtering out only those variable that showed high correlation with target - didn't account for many to one relations

2. Filtering out variables that were too dependent on each other, again error margin increased, because many to many relations were ignored.

3. The data was broken into small modules to prevent system from overworking.


The scripts and models are contained inside modules folder
There are three main scripts:

1. extraction.py - Extracts data from mongoDB in small packets and forms seperate json file of them.

2. train_model.py - Train the model on data extracted from MongoDB

3. test.py - Test the performance of model using RMSE and R2 scrore.
