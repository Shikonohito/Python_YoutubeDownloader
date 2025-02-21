class ItagError(Exception):
    "Raised when the itag not found."

    def __init__(self, message="Itag not found."):
        self.message = message
        super().__init__(self.message)