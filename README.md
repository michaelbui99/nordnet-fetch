# Nordnet Fetch

Convience script to store my Nordnet transactions and performance graphs

## Overview

![Solution overview](./doc/nordnet-fetch.drawio.png)

## Development Environment

### Requirements

-   Python 3+ (Developed in 3.11.0)

### Setup

#### Clone project

```cli
$ git clone https://github.com/michaelbui99/nordnet-fetch.git
```

#### Create virtual environment

```cli
$ cd ./nordnet-fetch
```

```cli
$ python -m venv .venv
```

#### Activate virtual environment (windows)

```cli
$ .\.venv\Scripts\activate
```

#### Install dependencies

```cli
$ pip install -r .\requirements.txt
```

#### Configure config.json

Set the transactionsOutputPath and performanceGraphOutputPath e.g:

```json
{
    "transactionsOutputPath": "C:\\Users\\Bruger\\Documents\\nordnet\\Transaktioner\\transactions",
    "performanceGraphOutputPath": "C:\\Users\\Bruger\\Documents\\nordnet\\Performance\\performance_graph"
}
```
