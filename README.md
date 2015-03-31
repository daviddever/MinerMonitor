MinerMonitor
============

Script for monitoring bitcoin miner hashing through ghash.io's api.
Sends an alert email when mining drops below threshold.

Installation
------------

The following assumes Ubuntu 14.04 64-bit

### Install pip

```
sudo apt-get install python-pip
sudo pip install -U pip
```

### Setup Virtualenv

```
sudo pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### Install script requirements

```
pip install -r requirements.txt
```

### Activate API

On https://cex.io/trade/profile activate the API for workers only.

### Get Python API module

Get cexapi.py from GANDERS fork of cex.io-api-python 
https://github.com/ganders/cex.io-api-python

### Configure config_example.py

Configure information in config_example.py and rename config.py

### Start the script

```
python monitor.py &
``` 

