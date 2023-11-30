class UserInputException(Exception):
    def __init__(self, message: str = "Wrong user input"):
        super().__init__(message)
