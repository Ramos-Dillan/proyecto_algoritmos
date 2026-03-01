from flask import jsonify

def success_response(data=None, message="Operación exitosa", status=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status


def error_response(message="Ocurrió un error", status=400):
    return jsonify({
        "success": False,
        "message": message,
        "data": None
    }), status