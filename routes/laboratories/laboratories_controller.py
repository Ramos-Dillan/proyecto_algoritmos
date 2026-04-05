from common.http import ok, bad_request
from routes.laboratories import laboratories_service


def getAll():
    data, error = laboratories_service.getAll()

    if error:
        return bad_request(
            message="No se pudieron obtener los laboratorios",
            errors=error
        )

    return ok(
        data=[{
            "id": d.id,
            "name": d.name
        } for d in data],
        message="Laboratorios obtenidos con éxito"
    )


def createLaboratory(data):
    result, error = laboratories_service.createLaboratory(data)

    if error:
        return bad_request(
            message="Error creando laboratorio",
            errors=error
        )

    return ok(
        data={
            "id": result.id,
            "name": result.name
        },
        message="Laboratorio creado correctamente"
    )


def deleteLaboratory(id):
    result, err = laboratories_service.deleteLaboratory(id)

    if err:
        return bad_request(
            message="Error eliminando laboratorio",
            errors=err
        )

    return ok(
        data={"delete": result},
        message=f"Laboratorio con id {id} eliminado correctamente"
    )


def updateLaboratory(id, data):
    result, err = laboratories_service.updateLaboratory(id, data)

    if err:
        return bad_request(
            message="Error actualizando laboratorio",
            errors=err
        )

    return ok(
        data={
            "update": {
                "id": result.id,
                "name": result.name
            }
        },
        message=f"Laboratorio con id {id} actualizado correctamente"
    )