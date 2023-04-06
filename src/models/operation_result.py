from enum import Enum

class OperationResult(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PROCESSING = "processing"
    