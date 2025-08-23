from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Ponto",
    description="API para gerenciamento de ponto de funcionários",
    version="0.0.1",
    contact={
        "name": "Luiz Claudio",
        "email": "luizclaudio_azeveo@hotmail.com"
    }
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sistema de Ponto API"}