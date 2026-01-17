from fastapi import FastAPI
from sqladmin import Admin, ModelView

from database.admin.empresas import EmpresasAdmin
from database.admin.empresas_usuarios_perfis import EmpresasUsuariosPerfisAdmin
from database.admin.usuarios import UsuariosAdmin
from database.db import Database
from database.models.empresas import Empresas
from routes.empresas import EmpresasRouter
from routes.usuarios import UsuariosRouter

app = FastAPI(
    title="Sistema de Ponto",
    description="API para gerenciamento de ponto de funcionários",
    version="0.0.1",
    contact={
        "name": "Luiz Claudio",
        "email": "luizclaudio_azeveo@hotmail.com"
    }
)

db= Database()
admin = Admin(app,db.engine, title="Administração do Sistema de Ponto")
admin.add_view(EmpresasAdmin)
admin.add_view(UsuariosAdmin)
admin.add_view(EmpresasUsuariosPerfisAdmin)


app.include_router(EmpresasRouter())
app.include_router(UsuariosRouter())
