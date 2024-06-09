from ariadne import ObjectType, gql, make_executable_schema
from ariadne.asgi import GraphQL
type_defs = gql(
    """
    type Query {
        usuario(id: ID!): Usuario
        usuarios: [Usuario]
    }

    type Mutation {
        crearUsuario(id: ID!, nombre: String!, apellido: String!, dni: Int!): Usuario
    }

    type Usuario {
        id: ID!
        nombre: String!
        apellido: String!
        dni: Int!
    }
    """
)
usuarios = [
    {"id": "1", "nombre": "Sergio", "apellido": "Pérez", "dni": 12345678},
    {"id": "2", "nombre": "Max", "apellido": "Verstappen", "dni": 87654321}
]

queries = ObjectType("Query")

@queries.field("usuario")
def resolve_usuario(_, info, id):
    for usuario in usuarios:
        if usuario["id"] == id:
            return usuario
    return None

@queries.field("usuarios")
def resolve_usuarios(_, info):
    return usuarios

mutaciones=ObjectType("Mutation")

@mutaciones.field("crearUsuario")
def resolve_crear_usuario(_, info, id, nombre, apellido, dni):
    nuevo_usuario = {
        "id": id,
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni
    }
    usuarios.append(nuevo_usuario)
    return nuevo_usuario


schema = make_executable_schema(type_defs, queries,mutaciones)

app = GraphQL(schema, debug=True)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")