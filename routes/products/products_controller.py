from common.http import ok, bad_request
from routes.products import products_service


def getAll():
    data, error = products_service.getAll()

    if error:
        return bad_request(
            message="No se pudieron obtener los productos",
            errors=error
        )

    return ok(
        data=[d.to_dict() for d in data],
        message="Productos obtenidos con éxito"
    )


def createProduct(data):
    result, error = products_service.createProduct(data)

    if error:
        return bad_request(
            message="Error creando producto",
            errors=error
        )

    return ok(
        data=result.to_dict(),
        message="Producto creado correctamente"
    )


def deleteProduct(id):
    result, err = products_service.deleteProduct(id)

    if err:
        return {"message": "error deleting product", "error": err}, 400

    return {
        "data": {"delete": result},
        "message": "Product with id " + str(id) + " delete successfully"
    }, 200


def updateProduct(id, data):
    result, err = products_service.updateProduct(id, data)

    if err:
        return bad_request(
            message="Error updating product",
            errors=err
        )

    return ok(
        data={"update": result.to_dict()},
        message=f"Product with id {id} updated successfully"
    )