from common.http import ok, bad_request
from routes.roles import roles_service


def getAll():
    data, error = roles_service.getAll()

    if error:
        return bad_request(
            message="No se pudieron obtener los roles",
            errors=error
        )

    return ok(
        data=[{
            "id": d.id,
            "name": d.name
        } for d in data],
        message="Roles obtenidos con éxito"
    )

def createRole(data):
    result, error = roles_service.createRole(data)

    if error:
        return bad_request(
            message="Error creando rol",
            errors=error
        )

    return ok(
        data={
            "id": result.id,
            "name": result.name
        },
        message="Rol creado correctamente"
    )