import os
import pickle
from cryptography.fernet import Fernet
import portalocker
import platform

class PersistentMemory:
    appFolder = None
    encryptionKey = None

    def __init__(self, appName, encryptionKey) -> None:
        self.appFolder = self.getAppFolder(appName)
        self.encryptionKey = encryptionKey
        # Additional initialization code (e.g., folder creation, key validation) goes here

        # check if the folder exists and create it if it doesn't
        if not os.path.exists(self.appFolder):
            os.makedirs(self.appFolder)


    def listKeys(self):
        keys = []
        try:
            # List all files in the appFolder
            if self.appFolder and os.path.exists(self.appFolder):
                keys = [f for f in os.listdir(self.appFolder) if os.path.isfile(os.path.join(self.appFolder, f))]
        except Exception as e:
            print(f"Error listing keys: {e}")
        
        return keys

    def push(self, key, data):
        # Serialize data
        serializedData = pickle.dumps(data)

        # check if data is None
        if serializedData is None:
            # if exists, delete the file
            filePath = os.path.join(self.appFolder, key)
            if os.path.exists(filePath):
                os.remove(filePath)
            return

        # Encrypt data
        if isinstance(self.encryptionKey, str):
            encryptionKeyBytes = self.encryptionKey.encode()
        else:
            encryptionKeyBytes = self.encryptionKey

        fernet = Fernet(encryptionKeyBytes)
        encryptedData = fernet.encrypt(serializedData)

        # Write to file with locking
        filePath = os.path.join(self.appFolder, key)
        with open(filePath, 'wb') as file:
            # Lock the file before writing
            portalocker.lock(file, portalocker.LOCK_EX)
            file.write(encryptedData)
            # The lock is automatically released when the file is closed

    def get(self, key):
        filePath = os.path.join(self.appFolder, key)

        # Check if the file exists
        if not os.path.exists(filePath):
            return None

        # Read and decrypt the data
        with open(filePath, 'rb') as file:
            encryptedData = file.read()

        fernet = Fernet(self.encryptionKey)
        try:
            decryptedData = fernet.decrypt(encryptedData)
        except Exception as e:
            # Handle decryption error
            print(f"Error during decryption: {e}")
            return None

        # Deserialize the data
        try:
            return pickle.loads(decryptedData)
        except Exception as e:
            # Handle deserialization error
            print(f"Error during deserialization: {e}")
            return None
        
    def __getattr__(self, name):
        # Attempt to fetch the data using the 'get' method
        return self.get(name)
    
    def __setattr__(self, name, value):
        # Check if setting a predefined attribute
        if name in ["appFolder", "encryptionKey", "initialize", "push", "get", "__getattr__", "__setattr__"]:
            # Handle as normal attribute
            self.__dict__[name] = value
        else:
            # Handle as a data key
            self.push(name, value)

    def getAppFolder(self, appName):
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


if __name__ == '__main__':
    persistentMemory = PersistentMemory('firstFolder', b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg=')
    # persistentMemory.data_0='methmet'
    print(persistentMemory.data_0)