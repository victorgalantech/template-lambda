"""
AWS Lambda handler for processing events.
"""

import json
import logging
from typing import Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    Main Lambda handler function.

    Args:
        event: The event dict containing the parameters sent when the function is invoked
        context: The context object containing runtime information

    Returns:
        Dict containing statusCode and body with response message
    """
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        # Extract data from event
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)

        name = body.get("name", "World")

        # Process the request
        result = process_request(name)

        # Return success response
        response = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps(
                {"message": result, "request_id": context.request_id if context else "local"}
            ),
        }

        logger.info(f"Returning response: {response}")
        return response

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Internal server error", "message": str(e)}),
        }


def process_request(name: str) -> str:
    """
    Process the incoming request.

    Args:
        name: The name to greet

    Returns:
        A greeting message
    """
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string")

    return f"Hello, {name}! Welcome to AWS Lambda."


def validate_input(data: Any) -> bool:
    """
    Validate input data.

    Args:
        data: The input data to validate

    Returns:
        True if valid, False otherwise
    """
    # Return the condition directly (Ruff SIM103)
    return isinstance(data, dict)
