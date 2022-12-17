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

#### Configuration

-   Rename .env.sample to .env
-   Fill out .env

```
NORDNET_USERNAME=myUsername123
NORDNET_PASSWORD=myPassword123
TRANSACTIONS_OUTPUT_PATH=PATH/TO/STORE/TRANSACTIONS/FILENAME
PERFORMANCE_GRAPH_OUTPUT_PATH=PATH/TO/STORE/PERFORMANCE_GRAPH_DATA/FILENAME
```
