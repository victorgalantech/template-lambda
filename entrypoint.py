"""
Entrypoint for AWS Lambda function.
This file serves as the main entry point and delegates to the actual handler.
Can be run locally for testing: python entrypoint.py
"""
import json
import logging
from src.lambda_handler import lambda_handler

# Re-export the handler for Lambda to invoke
__all__ = ['lambda_handler']


if __name__ == "__main__":
    # Configure logging for local execution
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    print("=" * 70)
    print("Running Lambda Function Locally")
    print("=" * 70)
    
    # Run local tests when executed directly
    test_cases = {
        "name": "The test case name - Victor - Custom Name",
        "event": {
            "body": json.dumps({"name": "Victor Galan"})
        }
    }
    
    print(f"\nInput Event: {json.dumps(test_cases['event'], indent=2)}\n")
    
    # Call the handler
    response = lambda_handler(test_cases['event'], None)
    
    print(f"\nResponse:")
    print(f"  Status Code: {response['statusCode']}")
    print(f"  Body: {response['body']}")
    print("\n" + "=" * 70)
