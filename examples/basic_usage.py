
# Example Usage of PersistentMemory

from persistentMemory.PersistentMemory import PersistentMemory

# Create an instance of PersistentMemory
pm = PersistentMemory(appName='ExampleApp', encryptionKey='ExampleKey')

# Example of storing data
pm.store_data('example_key', 'example_value')

# Example of retrieving data
retrieved_data = pm.retrieve_data('example_key')
print(retrieved_data)

