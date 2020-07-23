# Binary Independence Model

This was my first project in Python so most of the implementation may be naive and may not be pythonic. But the code works perfectly fine. 

There are 32604 news in the dataset. Programs ask you a query (what you want to search) and gives you the most relevant news articles. Just working like a search engine. 

## Parameters
There are only two parameters. Because the dataset set is large and it takes 30/40 minutes to process all of them. You can work with small number of examples by setting "trainingSetCount" equal to 100 or maybe 1000. "numberOfSearchesToShow" is the number of results returned by the algorithm. 

```python
##----------------------------
trainingSetCount = 32604
numberOfSearchesToShow = 5
##----------------------------
```

## Refrences Material
[BIM by Standford](https://nlp.stanford.edu/IR-book/html/htmledition/the-binary-independence-model-1.html) /
[Derrivation of BIM](https://nlp.stanford.edu/IR-book/essir2011/pdf/11prob.pdf)