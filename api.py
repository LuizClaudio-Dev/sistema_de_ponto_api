from fastapi import FastAPI

from routes.empresas import EmpresasRouter

app = FastAPI(
    title="Sistema de Ponto",
    description="API para gerenciamento de ponto de funcionários",
    version="0.0.1",
    contact={
        "name": "Luiz Claudio",
        "email": "luizclaudio_azeveo@hotmail.com"
    }
)

app.include_router(EmpresasRouter())
