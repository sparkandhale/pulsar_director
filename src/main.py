# use threads instead of processes to avoid being locked by the kafka topics (by sharing the underlying TCP connection)
import time
import sys, utils, traceback, uuid
import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
# needed in environments like application servers or Juphyter to nest the asyncio
# import nest_asyncio
# nest_asyncio.apply()
from famodels.models.trading_signal import TradingSignal
from famodels.models.state_of_signal import StateOfSignal
import globallogger
from src.models.api_response import APIResponse
from src.models.operation_result import OperationResult
from src.services.raw_signal_service import RawSignalService
from pathlib import Path
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse,JSONResponse

# CAUTION: only the main file should create this custom loger. The others should retrieve it. logging.getLogger('app)
logger = globallogger.setup_custom_logger('app')
logger.info(f"Starting {utils.get_application_name()}.")
logger.info(f"Logging Level is set to {utils.get_logging_level()}.")

tags_metadata = [
    {
        "name": "fa-signal-receiver",
        "description": "Send signals to our plattform. The **login** logic is also documente here.",
    }
]

app = FastAPI(
    #root_path="/signal-ingress",
    #openapi_url="/signal-ingress/openapi.json",
    #docs_url="/signal-ingress/docs",
    title="Pulsar Director", 
    openapi_tags=tags_metadata,    
    version="0.1.0",
    description="API Service",
    terms_of_service="https://signal-supplier.freya-alpha.com/terms",
    contact={
        "name": "Office of Operations",
        "url": "http://www.sparkandhale.com",
        "email": "hello@sparkandhal.com",
    },
    servers=[
        {"url": "http://localhost:8020", "description": "Development environment"},    
        {"url": "https://[your-host]", "description": "Production environment"},
        {"url": "https://[your-host]", "description": "Test environment"},
    ],
    
)

# CORS    
origins = [
    "http://127.0.0.1:8010",
    "http://127.0.0.1:8020",
    "http://0.0.0.0:8010",
    "http://localhost:8010",
    "https://fa-signal-receiver.freya-alpha.com",
    "https://fa-signal-receiver.integration.freya-alpha.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    #allow_origin_regex = "https://.*\.freya-alpha\.com",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use this request to modify the response for the validation error.
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=422)

@app.get("/")
async def main(request: Request):
    return [{"heartbeat": "alive"}, {"root_path": request.scope.get("root_path")}]

@app.get("/topics/{topic_name}")
async def get_topic(topic_name: str, request: Request):
    return topic_name


# @app.post("/topic/message", response_model=APIResponse, status_code=201, )
# async def submit_signal(signal: TradingSignal):
#     """Get List of Topics"""
#     logger.info(f"Received a signal: {signal}")
#     # Set the timestamp of registration and save the raw signal.
#     signal.timestamp_of_registration = int(time.time() * 1000)
#     if signal.id is not None and len(signal.provider_signal_id) == 0:
#         signal.provider_signal_id = signal.id
#     signal.id =  str(uuid.uuid4())
#     try: 
#         RawSignalService().produce_raw_signal(signal)        
#     except Exception as ex:
#         extype, ex, tb = sys.exc_info()
#         # Hide the real error, but log it.
#         logger.error(f"Failed to produce/insert a raw signal into the raw-signals topic. {ex} {traceback.print_exc()}. Signal: {signal.id}")
#         errMsg = f"We could not store your signal. Please modify your content. {ex} {traceback.print_exc()}. Signal: {signal.id}"
#         #TODO thsi needs to return a server error / or inaceptable content http code.
#         api_resp = APIResponse(operation_result=OperationResult.FAILURE, 
#                             signal_state=StateOfSignal.REJECTED,
#                             operation_details= errMsg)
#         return JSONResponse(api_resp.dict(), status_code=422)

#     # TODO what stupid model! also, why an extra CLASS/ROUTER FOR THIS? IT'S A CQRS pattern - just the command - never a query.
#     logger.info(f"Successfully stored a signal in the raw-signals topic: {signal.id}")  
        
#     return APIResponse(operation_result=OperationResult.SUCCESS, 
#                        signal_state=StateOfSignal.SUBMITTED, 
#                        supplier_signal_id=signal.provider_signal_id)
#     # Send the raw signal through the qualification process. DO NOT AWAIT THE RESPONSE.


if __name__ == "__main__":
    # This command is used to local development only. Otherwise the application is started with the dockerfile CMD.
    # In the local host, we don't use the root_path because there is no Proxy (Traefik) in between.
    #uvicorn.run(app, host="0.0.0.0", port=8020, log_level='debug', root_path="/signal-ingress")
    #uvicorn.run(app, host="0.0.0.0", port=8020, log_level='debug')
    print("RUNING WITH py src/main.py")