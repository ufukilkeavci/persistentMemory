
import unittest
from persistentMemory.PersistentMemory import PersistentDictionary

class TestPersistentMemory(unittest.TestCase):

    def setUp(self):
        # Setup that runs before each test method
        self.__appName = 'PersistentMemoryTest'
        self.__encryptionKey = b'Znd89nxh0ztocWfeXo8SLIqwaj5EiieF8eqwi_7iE70='  # Use a proper key for actual testing
        self.persistentMemory = PersistentDictionary(appName=self.__appName)
        self.persistentMemoryEncrypted = PersistentDictionary(appName=self.__appName, encryptionKey=self.__encryptionKey)

    def test_initialization(self):
        # Test initialization
        self.assertIsNotNone(self.persistentMemory)

    def test_data_storage_and_retrieval(self):
        # Test storing and retrieving data without encryption
        test_key = 'test_key'
        test_data = 'test_value'
        # Store data
        self.persistentMemory.test_key = test_data
        # Retrieve and assert the retrieved data is as expected
        retrieved_data = self.persistentMemory.test_key
        if retrieved_data is None:
            self.fail("Data retrieval failed.")
        else:
            self.assertEqual(test_data, retrieved_data)

    def test_data_storage_and_retrieval_with_encryption(self):
        # Test storing and retrieving data with encryption
        test_key = 'test_key'
        test_data = 'test_value'
        # Store data
        self.persistentMemoryEncrypted.test_key = test_data
        # Retrieve and assert the retrieved data is as expected
        retrieved_data = self.persistentMemoryEncrypted.test_key
        if retrieved_data is None:
            self.fail("Data retrieval failed.")
        else:
            self.assertEqual(test_data, retrieved_data)


    def test_error_handling(self):
        # Test error handling (e.g., wrong encryption key, file access issues)
        # You might want to use with self.assertRaises(ErrorType): in this section
        pass

    # Add more tests as needed for comprehensive coverage

if __name__ == '__main__':
    unittest.main()
