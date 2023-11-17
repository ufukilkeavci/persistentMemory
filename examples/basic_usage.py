
# Updated Example Usage of PersistentMemory

from persistentMemory.PersistentMemory import PersistentMemory

# Create an instance of PersistentMemory
pm = PersistentMemory(appName='ExampleApp', encryptionKey='ExampleKey')

# Storing data using attribute-style assignment and push method
pm.example_key = 'example_value'
pm.push('example_key', 'example_value')

# Retrieving data using attribute-style access and get method
retrieved_data_attr = pm.example_key
print('Retrieved data (attribute-style):', retrieved_data_attr)

retrieved_data_get = pm.get('example_key')
print('Retrieved data (get method):', retrieved_data_get)

# Demonstrating the caching mechanism (retrieve again to see the cache in action)
retrieved_data_cached = pm.get('example_key')
print('Retrieved from cache:', retrieved_data_cached)

# When needed, clear the cache
pm.clearCache()
