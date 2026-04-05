from common.http import ok, bad_request
from routes.therapeutic_groups import therapeutic_groups_service


def getAll():
    data, error = therapeutic_groups_service.getAll()

    if error:
        return bad_request(
            message="No se pudieron obtener los grupos terapéuticos",
            errors=error
        )

    return ok(
        data=[d.to_dict() for d in data],
        message="Grupos terapéuticos obtenidos con éxito"
    )


def createTherapeuticGroup(data):
    result, error = therapeutic_groups_service.createTherapeuticGroup(data)

    if error:
        return bad_request(
            message="Error creando grupo terapéutico",
            errors=error
        )

    return ok(
        data=result.to_dict(),
        message="Grupo terapéutico creado correctamente"
    )


def deleteTherapeuticGroup(id):
    result, err = therapeutic_groups_service.deleteTherapeuticGroup(id)

    if err:
        return {"message": "error deleting therapeutic group", "error": err}, 400

    return {
        "data": {"delete": result},
        "message": "Therapeutic group with id " + str(id) + " delete successfully"
    }, 200


def updateTherapeuticGroup(id, data):
    result, err = therapeutic_groups_service.updateTherapeuticGroup(id, data)

    if err:
        return bad_request(
            message="Error updating therapeutic group",
            errors=err
        )

    return ok(
        data={"update": result.to_dict()},
        message=f"Therapeutic group with id {id} updated successfully"
    )