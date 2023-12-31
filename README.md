
# PersistentMemory Library Documentation

## Overview
`PersistentMemory` is a Python library for managing persistent data with optional encryption. It provides a simple interface for storing and retrieving data, with an added benefit of in-memory caching for improved read performance.

## Installation
You can install the library using pip:
```
pip install PersistentMemory
```

## Usage

### Initialization
To use `PersistentMemory`, first import it and create an instance:
```python
from persistentMemory.PersistentMemory import PersistentDictionary
pd = PersistentDictionary(appName='YourAppName', encryptionKey='YourEncryptionKey')
```

### Storing Data
You can store data using the `store_data` method:
```python
pd.your_key = your_data
pd.push('your_key', your_data)
```

### Retrieving Data
Retrieve data using the `retrieve_data` method. This method will first check the in-memory cache before accessing the disk:
```python
data = pd.your_key
data = pd.get('your_key')
```

## Caching
Data read from disk is cached in memory, which speeds up subsequent read operations for the same data.

## Features
- Data persistence on the filesystem.
- Data encryption.
