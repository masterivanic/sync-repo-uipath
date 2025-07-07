
class PlatformException(Exception):
    def __init__(self, message="Only windows platform is supported"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
    
class GitNotFoundExeception(Exception):
    def __init__(self, message="git is not installed on this device"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
    
class UiPathNotFoundExeception(Exception):
    def __init__(self, message="UiPath software is not installed in this device"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message