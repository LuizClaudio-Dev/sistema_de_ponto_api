
import datetime
import json
from typing import List

from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse

from database.db import Database
from database.models import Empresas
from models.empresas import GetEmpresa
from utils import error_message


class EmpresasRouter(APIRouter):

    def __init__(self):
        super().__init__(prefix="/empresas", tags=["Empresas"])

        self.add_api_route('',
                           self.get_empresas,
                           methods=['GET'],
                           status_code=200,
                           response_model=List[GetEmpresa])

        self.add_api_route('/{id_empresa}',
                           self.get_empresa_by_id,
                           methods=['GET'],
                           status_code=200)

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
                    model_list_empresas = [GetEmpresa.model_validate(
                        empresa).model_dump() for empresa in db_empresas]
                    model_list_empresas = json.loads(json.dumps(
                        model_list_empresas, default=lambda o: o.isoformat() if isinstance(o, datetime) else o))
                else:
                    raise HTTPException(404, "Nenhuma empresa encontrada")
            return JSONResponse(model_list_empresas, 200)
        except Exception as E:
            error_message(E)

    def get_empresa_by_id(self, id_empresa: int = Path(..., gt=0)):
        try:
            with Database() as db:
                db_empresa = db.query(Empresas).get(id_empresa)
                if db_empresa:
                    model_empresa = GetEmpresa.model_validate(
                        db_empresa).model_dump()
            return JSONResponse(model_empresa, 200)
        except Exception as E:
            error_message(E)
