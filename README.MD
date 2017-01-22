# RSS-feed categorizer
### Idea
This idea of this project was to implement a web application which was capable of:
 - parse live RSS feeds
 - train a classifier on these feeds
 - predict the class of arbitrary input

Additional features:
  - Add new RSS feeds live
  - Retrain the classifier with additional data

Internally the application uses Stochastic Gradient Descent classifier `SGDClassifier()` with the best possible parameters returned by Grid Search `GridSearchCV()`, both of the methods are implemented in `sklearn`. Initial data is tokenized and vectorized using `CountVectorizer()` and transformed to normalized if-idf representation with `TfidfTransformer()`
```python
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier()),
])

parameters = {
    'vect__max_df': (0.5, 0.75, 1.0),
    'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
    'clf__alpha': (0.00001, 0.000001),
    'clf__penalty': ('l2', 'elasticnet'),
}
```
 
### Usage
Run `controllers.py` which will import the initial RSS feeds and start polling for additional data. 
The default front-end setup page is  `localhost:8080/scrap`. 

### Implementation
The main dependencies:
 - `cherrypy` web framework
 - `mako.template` templating engine 
 - `feedparser` scraping RSS feeds
 - `BeautifulSoup` parsing HTML
 - `sklearn` training the classifier
 


### MIT License:
<pre>
Copyright (c) 2017 Hannes Metssalu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</pre>
