from common.http import ok, bad_request
from routes.categories import categories_service


def getAll():
    data, error = categories_service.getAll()

    if error:
        return bad_request(
            message="No se pudieron obtener las categorías",
            errors=error
        )

    return ok(
        data=[{
            "id": d.id,
            "name": d.name
        } for d in data],
        message="Categorías obtenidas con éxito"
    )


def createCategory(data):
    result, error = categories_service.createCategory(data)

    if error:
        return bad_request(
            message="Error creando categoría",
            errors=error
        )

    return ok(
        data={
            "id": result.id,
            "name": result.name
        },
        message="Categoría creada correctamente"
    )


def deleteCategory(id):
    result, err = categories_service.deleteCategory(id)

    if err:
        return bad_request(
            message="Error eliminando categoría",
            errors=err
        )

    return ok(
        data={"delete": result},
        message=f"Categoría con id {id} eliminada correctamente"
    )


def updateCategory(id, data):
    result, err = categories_service.updateCategory(id, data)

    if err:
        return bad_request(
            message="Error actualizando categoría",
            errors=err
        )

    return ok(
        data={
            "update": {
                "id": result.id,
                "name": result.name
            }
        },
        message=f"Categoría con id {id} actualizada correctamente"
    )