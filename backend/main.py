# ==================== IMPORTS ====================
import os
import datetime
import pytz
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator

# Import logger from custom logging configuration
from logger_config import logger

# ==================== PYDANTIC MODELS ====================
class BatchOperation(BaseModel):
    operation: str
    numbers: List[float]

class BatchOperations(BaseModel):
    operations: List[BatchOperation]

# ==================== APP INITIALIZATION ====================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATABASE CONFIGURATION ====================
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb://admin_user:web3@localhost:27017/?authSource=admin"
)

mongo_client = MongoClient(MONGO_URL)
database = mongo_client.practica1
collection_historial = database.historial

# ==================== PROMETHEUS INSTRUMENTATION ====================
# Instrument the app with Prometheus metrics and expose /metrics endpoint
instrumentator = Instrumentator().instrument(app).expose(app)

# ==================== UTILITY FUNCTIONS ====================
def get_datetime():
    """Function to get date in Mexico timezone"""
    mexico_tz = pytz.timezone('America/Mexico_City')
    utc_now = datetime.datetime.now(pytz.UTC)
    mexico_time = utc_now.astimezone(mexico_tz)
    return mexico_time.strftime('%d/%m/%Y %H:%M')

def create_custom_error(error_message: str, operation: str, operands: list, status_code: int = 400):
    """Function to generate custom errors in JSON format"""
    error_response = {
        "error": error_message,
        "operation": operation,
        "operands": operands
    }
    return JSONResponse(status_code=status_code, content=error_response)

# ==================== VALIDATION FUNCTIONS ====================
def validate_numbers(a: float, b: float):
    """Validation function for two numbers"""
    if a < 0 or b < 0:
        raise HTTPException(status_code=400, detail="Negative numbers are not allowed")

def validate_numbers_list(numbers: List[float], operation: str):
    """Helper function for validating multiple numbers"""
    if len(numbers) < 2:
        return create_custom_error(
            "At least 2 numbers are required",
            operation,
            numbers,
            400
        )
    
    for num in numbers:
        if num < 0:
            return create_custom_error(
                "Negative numbers are not allowed",
                operation,
                numbers,
                400
            )
    return None

# ==================== MATHEMATICAL OPERATIONS ====================
def sum_multiple(numbers: List[float]):
    """Sum multiple numbers"""
    return sum(numbers)

def subtract_multiple(numbers: List[float]):
    """Subtract multiple numbers sequentially"""
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result

def multiply_multiple(numbers: List[float]):
    """Multiply multiple numbers"""
    result = 1
    for num in numbers:
        result *= num
    return result

def divide_multiple(numbers: List[float]):
    """Divide multiple numbers sequentially"""
    result = numbers[0]
    for num in numbers[1:]:
        if num == 0:
            return None  # Indicate division by zero error
        result /= num
    return result

# ==================== CALCULATOR ENDPOINTS ====================

@app.get("/calculator/sum")
def sum_endpoint(numbers: List[float] = Query(..., description="List of numbers to add")):
    """Sum operation endpoint"""
    # Number validation
    error = validate_numbers_list(numbers, "sum")
    if error:
        logger.error(f"sum validation error: numbers={numbers}")
        return error
    try:
        result = sum_multiple(numbers)
        
        # Save to history
        document = {
            "numbers": numbers,
            "result": result,
            "operation": "sum",
            "date": get_datetime()
        }
        collection_historial.insert_one(document)
        logger.info(f"sum completed: numbers={numbers}, result={result}")
        
        return {"numbers": numbers, "result": result}
    except Exception as e:
        logger.error(f"sum internal error: numbers={numbers}, error={str(e)}")
        return create_custom_error(f"Internal error: {str(e)}", "sum", numbers, 500)

@app.get("/calculator/substract")
def substract_endpoint(numbers: List[float] = Query(..., description="List of numbers to subtract")):
    """Subtract operation endpoint"""
    # Number validation
    error = validate_numbers_list(numbers, "subtract")
    if error:
        logger.error(f"subtract validation error: numbers={numbers}")
        return error
    try:
        result = subtract_multiple(numbers)
        
        # Save to history
        document = {
            "numbers": numbers,
            "result": result,
            "operation": "subtract",
            "date": get_datetime()
        }
        collection_historial.insert_one(document)
        logger.info(f"subtract completed: numbers={numbers}, result={result}")
        
        return {"numbers": numbers, "result": result}
    except Exception as e:
        logger.error(f"subtract internal error: numbers={numbers}, error={str(e)}")
        return create_custom_error(f"Internal error: {str(e)}", "subtract", numbers, 500)

@app.get("/calculator/multiply")
def multiply_endpoint(numbers: List[float] = Query(..., description="List of numbers to multiply")):
    """Multiplication operation endpoint"""
    # Number validation
    error = validate_numbers_list(numbers, "multiplication")
    if error:
        logger.error(f"multiplication validation error: numbers={numbers}")
        return error
    try:
        result = multiply_multiple(numbers)
        
        # Save to history
        document = {
            "numbers": numbers,
            "result": result,
            "operation": "multiplication",
            "date": get_datetime()
        }
        collection_historial.insert_one(document)
        logger.info(f"multiplication completed: numbers={numbers}, result={result}")
        
        return {"numbers": numbers, "result": result}
    except Exception as e:
        logger.error(f"multiplication internal error: numbers={numbers}, error={str(e)}")
        return create_custom_error(f"Internal error: {str(e)}", "multiplication", numbers, 500)

@app.get("/calculator/divide")
def divide_endpoint(numbers: List[float] = Query(..., description="List of numbers to divide")):
    """Division operation endpoint"""
    # Number validation
    error = validate_numbers_list(numbers, "division")
    if error:
        logger.error(f"division validation error: numbers={numbers}")
        return error
    
    # Check for division by zero
    for num in numbers[1:]:
        if num == 0:
            logger.error(f"division by zero attempt: numbers={numbers}")
            return create_custom_error(
                "Division by zero",
                "division",
                numbers,
                403
            )
    try:
        result = divide_multiple(numbers)
        
        # Save to history
        document = {
            "numbers": numbers,
            "result": result,
            "operation": "division",
            "date": get_datetime()
        }
        collection_historial.insert_one(document)
        logger.info(f"division completed: numbers={numbers}, result={result}")
        
        return {"numbers": numbers, "result": result}
    except Exception as e:
        logger.error(f"division internal error: numbers={numbers}, error={str(e)}")
        return create_custom_error(f"Internal error: {str(e)}", "division", numbers, 500)

# ==================== BATCH OPERATIONS ENDPOINT ====================

@app.post("/calculator/batch")
def batch_operations(request: List[BatchOperation]):
    """Endpoint for batch operations"""
    results = []
    
    for operation_data in request:
        operation = operation_data.operation
        numbers = operation_data.numbers
        
        # Validate that we have exactly 2 numbers
        if len(numbers) != 2:
            result = {
                "operation": operation,
                "error": "Exactly 2 numbers are required",
                "operands": numbers
            }
            results.append(result)
            logger.warning(f"batch invalid operands count: operation={operation}, operands={numbers}")
            continue
        
        a, b = numbers[0], numbers[1]
        
        # Validate negative numbers
        if a < 0 or b < 0:
            result = {
                "operation": operation,
                "error": "Negative numbers are not allowed",
                "operands": [a, b]
            }
            results.append(result)
            logger.warning(f"batch negative operands: operation={operation}, operands={[a, b]}")
            continue
        
        # Process according to operation type
        try:
            if operation == "sum":
                result = a + b
            elif operation == "sub":
                result = a - b
            elif operation == "mul":
                result = a * b
            elif operation == "div":
                if b == 0:
                    result = {
                        "operation": operation,
                        "error": "Division by zero",
                        "operands": [a, b]
                    }
                    results.append(result)
                    logger.warning(f"batch division by zero: operands={[a, b]}")
                    continue
                result = a / b
            else:
                result = {
                    "operation": operation,
                    "error": "Unsupported operation",
                    "operands": [a, b]
                }
                results.append(result)
                logger.warning(f"batch unsupported operation: operation={operation}, operands={[a, b]}")
                continue
            
            # If we get here, the operation was successful
            result = {
                "operation": operation,
                "result": result
            }
            results.append(result)
            logger.info(f"batch operation completed: operation={operation}, operands={[a, b]}, result={result['result']}")
            
            # Save to history
            document = {
                "a": a,
                "b": b,
                "result": result,
                "operation": operation,
                "date": get_datetime()
            }
            collection_historial.insert_one(document)
            
        except Exception as e:
            result = {
                "operation": operation,
                "error": f"Internal error: {str(e)}",
                "operands": [a, b]
            }
            results.append(result)
            logger.error(f"batch internal error: operation={operation}, operands={[a, b]}, error={str(e)}")
    
    return results

# ==================== PROMETHEUS INSTRUMENTATION ====================
# Instrument the app with Prometheus metrics
instrumentator = Instrumentator().instrument(app).expose(app)

# ==================== HISTORY ENDPOINT ====================

@app.get("/calculator/history")
def get_history():
    """Get operation history endpoint"""
    try:
        operations = collection_historial.find({})
        history = []
        
        for operation in operations:
            # Handle both string dates and datetime objects
            date_value = operation["date"]
            if isinstance(date_value, str):
                formatted_date = date_value
            else:
                # Convert datetime object to Mexico format
                mexico_tz = pytz.timezone('America/Mexico_City')
                if hasattr(date_value, 'astimezone'):
                    mexico_time = date_value.astimezone(mexico_tz)
                    formatted_date = mexico_time.strftime('%d/%m/%Y %H:%M')
                else:
                    formatted_date = str(date_value)
            
            # Handle both old and new field names for compatibility
            numbers = operation.get("numbers", operation.get("numeros", [operation.get("a"), operation.get("b")]))
            result = operation.get("result", operation.get("resultado"))
            operation_type = operation.get("operation", operation.get("operacion", "unknown"))
            
            history.append({
                "numbers": numbers,
                "result": result,
                "operation": operation_type,
                "date": formatted_date
            })

        return {"history": history}
    except Exception as e:
        logger.error(f"history internal error: error={str(e)}")
        return create_custom_error(f"Internal error: {str(e)}", "history", [], 500)
