from typing import Any, Union
from sqlmodel import SQLModel
from famodels.models.state_of_signal import StateOfSignal
from custom_models.operation_result import OperationResult
from fastapi.responses import JSONResponse

class APIResponse(SQLModel, table=False):
    operation_result: OperationResult
    signal_state: StateOfSignal    
    operation_details: str = None
    supplier_signal_id: str = None