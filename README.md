# FinEconometrics
A repository used for the project in Financial Econometrics

All code of the project is contained in src/. Only the raw input data before any data handling is contained in data/.

src/compiled_data contains versions of the transformed raw-input, after its pre-processing has completed.

src/models contains the model training results, as well as the hyperparameter-tuning plots which serve to visualise the results over their hyperparameter specification. In each subfolder of the specific models, the grid search results (hyperparameters utilized, and their accompanying performance) are contained in a gs_res.pkl file.

src/cleaning.ipynb contains the entirety of the procedure used for pre-processing, while src/Modelling.ipynb includes the modelling procedure. The model functions are written in src/models.py

Authors: amin.debabeche@epfl.ch, karim.alkhadzh@epfl.ch, xxx@epfl.ch, xxx@epfl.ch & xxx@epfl.ch

The following is the link who did similar projects before:
https://github.com/pimkarnm/NLP-Bitcoin,
https://github.com/Drabble/TwitterSentimentAndCryptocurrencies,
https://github.com/arapelli/Bitcoin-price-prediction-using-twitter-sentiment-analysis
