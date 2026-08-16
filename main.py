from fastapi import FastAPI

from src.routes.empresas import EmpresasRouter
from src.routes.usuarios import UsuariosRouter

app = FastAPI(
    title="Sistema de Ponto",
    description="API para gerenciamento de ponto de funcionários",
    version="0.0.1",
    contact={
        "name": "Luiz Claudio",
        "email": "luizclaudio_azevedo@hotmail.com"
    }
)


app.include_router(EmpresasRouter())
app.include_router(UsuariosRouter())
