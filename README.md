picasclient
===========

Python client using CouchDB as a token pool server.

## Installation

Run
```
pip install -U .
```

## Testing

First, install the test dependencies with 
```
pip install ".[test]"
```
To test, run
```
flake8 picas tests
nosetests tests
```
