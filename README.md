
# PersistentMemory Library Documentation

## Overview
`PersistentMemory` is a Python library for managing persistent data with optional encryption. It provides a simple interface for storing and retrieving data, with an added benefit of in-memory caching for improved read performance.

## Installation
You can install the library using pip:
```
pip install persistentMemory
```

## Usage

### Initialization
To use `PersistentMemory`, first import it and create an instance:
```python
from persistentMemory.PersistentMemory import PersistentMemory
pm = PersistentMemory(appName='YourAppName', encryptionKey='YourEncryptionKey')
```

### Storing Data
You can store data using the `store_data` method:
```python
pm.your_key = your_data
pm.push('your_key', your_data)
```

### Retrieving Data
Retrieve data using the `retrieve_data` method. This method will first check the in-memory cache before accessing the disk:
```python
data = pm.your_key
data = pm.get('your_key')
```

## Caching
Data read from disk is cached in memory, which speeds up subsequent read operations for the same data.

## Features
- Data persistence on the filesystem.
- Data encryption.
- def get_user_profile_info(user_id):
-   user = db.query("SELECT * FROM Users WHERE id = %s", user_id)
-   return user

## API Reference
Provide detailed descriptions and examples for each public method in the class here.
