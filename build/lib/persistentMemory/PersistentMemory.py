import os
import pickle
from cryptography.fernet import Fernet
import portalocker
import platform

class PersistentMemory:
    __appFolder = None
    __encryptionKey = None
    __cache = {}

    def __init__(self, appName, encryptionKey=None):
        appFolder = self.__getAppFolder(appName)
        self.__appFolder = appFolder
        self.__encryptionKey = encryptionKey
        # Additional initialization code (e.g., folder creation, key validation) goes here
        self.__cache = {}  # Initialize an empty cache

        # check if the folder exists and create it if it doesn't
        if not os.path.exists(self.__appFolder):
            os.makedirs(self.__appFolder)
        


    def listKeys(self):
        keys = []
        try:
            # List all files in the appFolder
            if self.__appFolder and os.path.exists(self.__appFolder):
                keys = [f for f in os.listdir(self.__appFolder) if os.path.isfile(os.path.join(self.__appFolder, f))]
        except Exception as e:
            print(f"Error listing keys: {e}")
        
        return keys

    def push(self, key, data):
        
        # Diagnostic print for encryptionKey
        # Serialize data
        serializedData = pickle.dumps(data)

        self.__cache[key] = data
        # check if data is None
        if serializedData is None:
            # if exists, delete the file
            filePath = os.path.join(self.__appFolder, key)
            if os.path.exists(filePath):
                os.remove(filePath)
            return
        
        # Handle optional encryption
        if self.__encryptionKey:
            # Code to store value with encryption
            fernet = Fernet(self.__encryptionKey)
            dataToStore = fernet.encrypt(serializedData)
        else:
            # Code to store value without encryption
            dataToStore = serializedData
        

        # Write to file with locking
        filePath = os.path.join(self.__appFolder, key)
        with open(filePath, 'wb') as file:
            # Lock the file before writing
            portalocker.lock(file, portalocker.LOCK_EX)
            file.write(dataToStore)
            # The lock is automatically released when the file is closed

    def get(self, key):
        
        if key in self.__cache:
            return self.__cache[key]

        filePath = os.path.join(self.__appFolder, key)

        # Check if the file exists
        if not os.path.exists(filePath):
            return None

        # Read and decrypt the data
        with open(filePath, 'rb') as file:
            encryptedData = file.read()

        if self.__encryptionKey:
            fernet = Fernet(self.__encryptionKey)
            try:
                decryptedData = fernet.decrypt(encryptedData)
            except Exception as e:
                # Handle decryption error
                print(f"Error during decryption: {e}")
                return None
            dataFromFile = decryptedData
        else:
            dataFromFile = encryptedData
        # Deserialize the data
        try:
            return pickle.loads(decryptedData)
        except Exception as e:
            # Handle deserialization error
            print(f"Error during deserialization: {e}")
            return None
        
    def __getattr__(self, name):
        if self.is_method(name):
            return self.get_method(name)
        elif self.is_class_attribute(name):
            return self.get_class_attribute(name)
        else:
            return self.get(name)
    
    def __setattr__(self, name, value):
        # Check if setting a predefined attribute
        if self.is_class_attribute(name):
            # Handle as normal attribute
            self.__dict__[name] = value
        else:
            # Handle as a data key
            self.push(name, value)

    def is_method(self, name):
        return callable(getattr(self.__class__, name, None))

    def is_class_attribute(self, name):
        return name in self.__class__.__dict__

    def get_method(self, name):
        return getattr(self, name)

    def get_class_attribute(self, name):
        return getattr(self.__class__, name)

    def __getAppFolder(self, appName):
        """
        Returns the path to the application data folder based on the operating system.

        :param app_name: Name of the application
        :return: Path to the application data folder
        """
        osName = platform.system()

        if osName == 'Windows':
            # Path for Windows (typically in the Roaming directory)
            return os.path.join(os.environ['APPDATA'], appName)

        elif osName == 'Darwin':
            # Path for macOS (in the Application Support directory)
            return os.path.expanduser(f'~/Library/Application Support/{appName}')

        elif osName == 'Linux':
            # Path for Linux (hidden directory in the user's home directory)
            return os.path.expanduser(f'~/.{appName.lower()}')

        else:
            # For unknown OS, raise an error or handle as needed
            raise NotImplementedError(f"OS '{osName}' not supported.")
    
    def clearCache(self):
        """
        Clears the in-memory cache.
        """
        self.__cache = {}

if __name__=="__main__":
    pm = PersistentMemory("test")