# emovix-twitter-graph
Application to create a directional graph from the Followers and Friends of Twitter user accounts defined in a file.


## Prerequisites

 - Python 2.7
 - git
 - pip
 - virtualenv

## Installation

    git clone https://github.com/eMOVIX/emovix-twitter-graph.git
    cd emovix-twitter-graph
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Configuration

Add your Twitter API credentials to the configuration file:

    vim config.json

## Usage

    python emovix-twitter-graph.py
