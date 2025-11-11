import logging
import functions_framework
from flask import jsonify, Request

from handlers.tag_register import HANDLERS
from utils import df_error, BadRequestError, UpstreamError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dfcx-webhook")


def _parse_webhook_tag(req_body: dict) -> str:
    tag = (req_body.get("fulfillmentInfo") or {}).get("tag")
    if not tag:
        raise BadRequestError("Missing fulfillmentInfo.tag")
    if tag not in HANDLERS:
        raise BadRequestError(f"Invalid tag: {tag}")
    return tag


def _parse_parameters(req_body: dict) -> dict:
    return (req_body.get("sessionInfo") or {}).get("parameters") or {}


@functions_framework.http
def hello_http(request: Request):
    """Entry point for Dialogflow CX webhook (simplified trainer's version)."""
    try:
        req_body = request.get_json(silent=True) or {}
    except Exception:
        logger.error("Invalid JSON body")
        return jsonify(df_error(400, "Invalid JSON body")), 200

    logger.info("Incoming webhook")

    try:
        tag = _parse_webhook_tag(req_body)
        parameters = _parse_parameters(req_body)

        handler = HANDLERS[tag]
        df_response = handler(parameters)

        logger.info("Handler executed successfully: %s", tag)
        return jsonify(df_response), 200

    except BadRequestError as e:
        logger.warning("Bad request: %s", str(e))
        return jsonify(df_error(400, str(e))), 200

    except UpstreamError as e:
        logger.error("Upstream error: %s", str(e))
        return jsonify(df_error(502, "Upstream provider error")), 200

    except Exception as e:
        logger.exception("Unexpected error")
        return jsonify(df_error(500, "Internal error")), 200
