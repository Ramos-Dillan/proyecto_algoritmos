from common.http import ok, bad_request
from routes.products import products_service


def getAll():
    data, error = products_service.getAll()
    if error:
        return bad_request(message="No se pudieron obtener los productos", errors=error)
    return ok(data=data, message="Productos obtenidos con éxito")


def createProduct(data):
    result, error = products_service.createProduct(data)
    if error:
        return bad_request(message="Error creando producto", errors=error)
    return ok(data=result.to_dict(), message="Producto creado correctamente")


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
        return bad_request(message="Error updating product", errors=err)
    return ok(data=result, message=f"Product with id {id} updated successfully")  # ✅


def getById(id):
    data, err = products_service.getById(id)
    if err:
        return bad_request(message="Error obteniendo producto", errors=err)
    return ok(data=data, message="Producto obtenido con éxito")


def filter(params):
    items, total, err = products_service.filterProducts(params)
    if err:
        return bad_request(message="Error filtrando productos", errors=err)
    return ok(data={"items": items, "total": total}, message="Productos filtrados con éxito")

def toggleActive(id, data):
    result, err = products_service.toggleActive(id, data.get('is_active'))
    if err:
        return bad_request(message="Error actualizando estado", errors=err)
    return ok(data=result, message=f"Estado del producto {id} actualizado")  