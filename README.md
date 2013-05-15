dataroses
=========

A shameless reimplementation of the [nvd3.js](http://nvd3.org) based
graph generator web service that cannot be named (see
[datafart.com](http://datafart.com))


## Dependencies

- MongoDB for local graph caching

- https://github.com/jcborras/colorbrewer-python (FTTB)

## Usage

Pretty much like the unnamed.

- Send a CSV file over HTTP to an end URL depending on the graph you
  want to generate:

    curl --data-binary @- http://your_dataroses_server:port/lineChart < somedata.csv

- Access the resulting URL for the graph

- There are a few of the nvd3.js graphs ready to use. Just use a different end-URL.
