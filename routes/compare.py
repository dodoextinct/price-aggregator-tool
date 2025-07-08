from flask import Blueprint, request, jsonify
from workflows.price_comparison_flow import PriceComparisonWorkflow
import threading

compare_bp = Blueprint("compare", __name__)


@compare_bp.route("/compare", methods=["POST"])
def compare_prices():
    try:
        data = request.json
        query = data.get("query")
        country = data.get("country")
        session_id = data.get("session_id", "anon")

        if not query or not country:
            return (
                jsonify({"error": "Missing 'query' or 'country' in request body"}),
                400,
            )

        cancel_event = threading.Event()
        workflow = PriceComparisonWorkflow(session_id=session_id)

        result = workflow.run(
            query=query, country=country, cancel_event=cancel_event
        )
        return jsonify(result.content)

    except Exception as e:
        return jsonify({"error": "Server error occurred", "exception": str(e)}), 500
