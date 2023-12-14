from shared_types import Result, Ok, Err
import sys

def args_filepath() -> Result:
    if len(sys.argv) < 2:
        return Err(Exception("Please provide a filepath"))
    
    return Ok(sys.argv[1])