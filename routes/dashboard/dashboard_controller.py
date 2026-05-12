from flask import jsonify
from routes.dashboard.dashboard_service import get_summary as service_summary


def get_summary():
    data, error = service_summary()

    if error:
        return jsonify({
            "success": False,
            "error": error
        }), 500

    return jsonify({
        "success": True,
        "data": data
    }), 200