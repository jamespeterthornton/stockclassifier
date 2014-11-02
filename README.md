stockclassifier
===============

Classification: James Thornton and Dylan Hurwitz
Web Scraping: Thomas Thornton

This is a Naive Bayes text classifier. It classifies the Management Discussion and Analysis of a company's 10-Q, a quarterly report filed with the SEC.

To run the code, start the Python shell, import evaluation, and run eval("training_set.data"). This will split the training data (10-Qs for the Dow Jones Industrial Average) into five parts, and use cross-validation to gauge the accuracy of the classifier (training on four parts, testing on the fifth, and rotating the test segment until all possibilities have been measured). It will then generate nine more splits, do the same on each, and return the average accuracy from all of these results. Generally, we get about 65% accuracy for the basic classifier, closer to 70% with holds.

Note that holds are treated somewhat ficticiously, as no documents are pre-classified as "HOLD," but rather the classifier is allowed to "not bet" on reports that it is unsure of, and this is the purpose of the hold classification.

Feel free, also to modify the list of tickers at the end of scraper.py and use it to generate new training sets.