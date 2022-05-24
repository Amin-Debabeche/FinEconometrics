class PreProcessing:
    
    def __init__(self, data, lemmatize=True, lower_case=True, rem_stopwords=True, rem_punctuation=True):
        """
        Initialise all class parameters

        :param data: nonempty pandas dataframe, wsb dataframe 
        :param lemmatize: bool, whether to perform lemmatization
        :param lower_case: bool, whether to lowercase
        :param rem_stopwords: bool, whether to remove stopwords
        :param tokenize: bool, whether to tokenize
        """

        self.data = data
        self.lemmatize = lemmatize
        self.lower_case = lower_case
        self.rem_stopwords = rem_stopwords
        self.rem_punctuation = rem_punctuation

    # Ensure Parameter types
    # K: need to add to this one gradually as we add columns that we use etc.
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):

        req_columns = ['author', 'body', 'created_utc']
        str_columns = ['body']
        date_columns = ['created_utc']

        # Ensure the provided object is a dataframe
        if not isinstance(data, pd.DataFrame):
            raise Exception("The provided data must be a pandas Dataframe")

        # Ensure wsb dataframe is non empty
        if data.shape[0] == 0:
            raise Exception("Provided Dataframe is empty")

        # Ensure all required columns are provided
        missing_columns = set(req_columns).difference(
            set(data.columns.tolist()))
        if len(missing_columns) > 0:
            raise Exception(
                f"The columns {missing_columns} are missing from the provided dataframe!")

        # Ensure all column names don't have unexpected periods
        if '.' in list(''.join(data.columns.tolist())):
            raise Exception("All Column names must not include periods :'.'")

        # Ensure all string columns are strings
        non_str_columns = set(str_columns).difference(
            set(data.select_dtypes(include='object')))
        if len(non_str_columns) > 0:
            raise Exception(
                f'The columns {non_str_columns} are expected as string (pandas object) columns.')

        self._data = data

    @property
    def lemmatize(self):
        return self._lemmatize

    @lemmatize.setter
    def lemmatize(self, lemmatize):
        if not isinstance(lemmatize, bool) and lemmatize is not None:
            raise Exception(
                'lemmatize must be provided as a boolean parameter (True/False) or None to the class')
        self._lemmatize = lemmatize

    @property
    def lower_case(self):
        return self._lower_case

    @lower_case.setter
    def lower_case(self, lower_case):
        if not isinstance(lower_case, bool):
            raise Exception(
                'lower_case must be provided as a boolean parameter (True/False) to the class')
        self._lower_case = lower_case

    @property
    def rem_stopwords(self):
        return self._rem_stopwords

    @rem_stopwords.setter
    def rem_stopwords(self, rem_stopwords):
        if not isinstance(rem_stopwords, bool):
            raise Exception(
                'rem_stopwords must be provided as a boolean parameter (True/False) to the class')
        self._rem_stopwords = rem_stopwords

    @property
    def rem_punctuation(self):
        return self._rem_punctuation

    @rem_punctuation.setter
    def rem_punctuation(self, rem_punctuation):
        if not isinstance(rem_punctuation, bool):
            raise Exception(
                'rem_punctuation must be provided as a boolean parameter (True/False) to the class')
        self._rem_punctuation = rem_punctuation

#     @property
#     def tokenize(self):
#         return self._tokenize

#     @tokenize.setter
#     def tokenize(self, tokenize):
#         if not isinstance(tokenize, bool):
#             raise Exception(
#                 'tokenize must be provided as a boolean parameter (True/False) to the class')
#         self._tokenize = tokenize

    def clean_textual_data(self, textual_columns):

        # Ensure the provided textual columns exist, and if single string column name convert it into a list
        if len(textual_columns) < 1:
            raise Exception(
                'The number of textual columns to clean must be greater than 0')
        if isinstance(textual_columns, str):
            textual_columns = [textual_columns]
        missing_columns = set(textual_columns).difference(
            set(self.data.columns.tolist()))
        if len(missing_columns) > 0:
            raise Exception(
                f"The columns {missing_columns} to clean are missing from the wsb dataframe!")
            
        def rem_null(self, col_name):
            self.data = self.data[self.data[col_name].notna()]
            return self.data

        def lower_case_fn(self, col_name):
            self.data[col_name] = self.data[col_name].str.lower()
            return self.data

        def lemmatize_fn(self, col_name):
            w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
            lemmatizer = nltk.stem.WordNetLemmatizer()
            self.data[col_name] = self.data[col_name].apply(
                lambda x: [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(x)])
            return self.data

        def stemming_fn(self, col_name):
            w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
            stemmer = nltk.stem.porter.PorterStemmer()
            self.data[col_name] = self.data[col_name].apply(
                lambda x: [stemmer.stem(w) for w in w_tokenizer.tokenize(x)])
            return self.data

        def tokenize_fn(self, col_name):
            w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
            self.data[col_name] = self.data[col_name].apply(
                lambda x: [w for w in w_tokenizer.tokenize(x)])
            return self.data

        def rem_punctuation_fn(self, col_name):
            self.data[col_name] = self.data[col_name].apply(
                lambda x: [w for w in x if w.isalnum()])
            return self.data

        def rem_stopwords_fn(self, col_name):
            "stopwords dictionary considered English, wsb is an english forum"
            remove_elements = set(nltk.corpus.stopwords.words('english'))
            self.data[col_name] = self.data[col_name].apply(
                lambda x: [w for w in x if not w in remove_elements])
            return self.data

        def remove_tokenization(self, col_name):
            "Necessary as final step to untokenize in case desired, tokenization required for other functions to not break"
            self.data[col_name] = self.data[col_name].apply(
                lambda x: ' '.join(x))
            return self.data

        for textual_col in textual_columns:
            
            rem_null(self, textual_col)

            if self.lower_case:
                lower_case_fn(self, textual_col)

            # lemmatize tokens if true, if false, stem tokens, if None then just tokenize
            if self.lemmatize:
                lemmatize_fn(self, textual_col)
            elif self.lemmatize == False:
                stemming_fn(self, textual_col)
            else:
                tokenize_fn(self, textual_col)

            if self.rem_punctuation:
                rem_punctuation_fn(self, textual_col)
            if self.rem_stopwords:
                rem_stopwords_fn(self, textual_col)
                
            remove_tokenization(self, textual_col)

        return self.data