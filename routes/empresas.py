
from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse

from database.db import Database
from database.models.empresas import Empresas
from models.empresas import GetEmpresa


class EmpresasRouter(APIRouter):

    def __init__(self):
        super().__init__(prefix="/empresas", tags=["Empresas"])

        self.add_api_route('',
                           self.get_empresas,
                           methods=['GET'],
                           status_code=200, response_model=list[GetEmpresa])

        # self.add_api_route('/{id_empresa}',
        #                    self.get_empresa_by_id,
        #                    methods=['GET'],
        #                    status_code=200)

    def get_empresas(self,
                     ativo: int = Query(
                         1, alias="ativo", description="Se a empresa estiver ativa ou não", gt=0, lt=2),
                     pagina: int = Query(
                         1, alias="pagina", description="Número da página", gt=0),
                     limite: int = Query(
                         10, alias="limite", description="Número de registros por página", gt=0),
                     ):
        try:
            with Database() as db:
                db_empresas = db.query(Empresas).filter(Empresas.ativo == ativo).limit(
                    limite).offset((pagina - 1) * limite).all()
                if db_empresas:
                    model_list_empresas = [GetEmpresa.model_validate(empresa).model_dump() for empresa in db_empresas]
            return JSONResponse(model_list_empresas, 200)
        except Exception as E:
            if isinstance(E, HTTPException):
                raise E
            else:
                raise HTTPException(500, str(E))
