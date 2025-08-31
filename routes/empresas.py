from fastapi import APIRouter, Body, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from sqlalchemy import func

from database.db import Database
from database.models import Empresas
from schemas.empresas import ListEmpresas, SetEmpresa
from utils import (error_message, model_dict_json_serializer,
                   resposta_get_com_paginacao)


class EmpresasRouter(APIRouter):

    def __init__(self):
        super().__init__(prefix="/empresas", tags=["Empresas"])

        self.add_api_route('',
                           self.get_empresas,
                           methods=['GET'],
                           status_code=200,
                           response_model=ListEmpresas)

        self.add_api_route('/{id_empresa}',
                           self.get_empresa_by_id,
                           methods=['GET'],
                           status_code=200)

        self.add_api_route('',
                           self.set_empresa,
                           methods=['POST'],
                           response_model=SetEmpresa,
                           status_code=201)

        self.add_api_route('',
                           self.patch_empresa,
                           methods=['PATCH'],
                           status_code=200)

        self.add_api_route('/{id_empresa}',
                           self.delete_empresa,
                           methods=['DELETE'],
                           status_code=200)

    def get_empresas(self,
                     ativo: int = Query(
                         1, alias="ativo", description="Se a empresa estiver ativa ou não, escreva '-1' para todas", lt=2),
                     pagina: int = Query(
                         1, alias="pagina", description="Número da página", gt=0),
                     limite: int = Query(
                         10, alias="limite", description="Número de registros por página", gt=0),
                     ):
        try:
            model_list_empresas = ListEmpresas.model_construct()
            with Database() as db:

                total = db.query(func.count(Empresas.id_empresa)).filter(
                    Empresas.ativo == ativo if ativo != -1 else Empresas.ativo.in_([0, 1])).scalar()

                db_empresas = db.query(Empresas).filter(Empresas.ativo == ativo if ativo != -1 else Empresas.ativo.in_([0, 1])).limit(
                    limite).offset((pagina - 1) * limite).all()

                if not db_empresas:
                    raise HTTPException(404, "Nenhuma empresa encontrada")

                model_list_empresas.empresas = [model_dict_json_serializer(ListEmpresas.Empresa.model_validate(
                    empresa).model_dump()) for empresa in db_empresas]

            return JSONResponse(resposta_get_com_paginacao('empresas', model_list_empresas.empresas, total, pagina, limite), 200)
        except Exception as E:
            error_message(E)

    def get_empresa_by_id(self, id_empresa: int = Path(..., gt=0)):
        try:
            with Database() as db:
                db_empresa = db.query(Empresas).get(id_empresa)
                if db_empresa:
                    model_empresa = model_dict_json_serializer(ListEmpresas.Empresa.model_validate(
                        db_empresa).model_dump())
                else:
                    raise HTTPException(404, "Empresa não encontrada")
            return JSONResponse(model_empresa, 200)
        except Exception as E:
            error_message(E)

    def set_empresa(self, empresa_info: SetEmpresa = Body()):
        try:
            with Database() as db:
                db_empresa = Empresas(
                    **empresa_info.model_dump(exclude={'id_empresa'}))
                db.add(db_empresa)
                db.flush()
                db.refresh(db_empresa)
                if db_empresa.id_empresa:
                    empresa_info.id_empresa = db_empresa.id_empresa
                    db.commit()
            return JSONResponse(empresa_info.model_dump(mode='json'), 201)
        except Exception as E:
            error_message(E)

    def patch_empresa(self, empresa_info: SetEmpresa = Body()):
        try:
            with Database() as db:
                db_edit_empresa = db.query(Empresas).filter(Empresas.id_empresa == empresa_info.id_empresa).update(
                    empresa_info.model_dump(exclude={'id_empresa'}, exclude_unset=True))
                if db_edit_empresa:
                    db.commit()
                else:
                    raise HTTPException(404, "Empresa não encontrada")
            return JSONResponse({"detail": "Empresa alterada com sucesso!"}, 200)
        except Exception as E:
            error_message(E)

    def delete_empresa(self, id_empresa: int = Path(..., gt=0)):
        try:
            with Database() as db:
                db_delete_empresa = db.query(Empresas).filter(
                    Empresas.id_empresa == id_empresa).update({'ativo': 2})
                if db_delete_empresa:
                    db.commit()
                else:
                    raise HTTPException(404, "Empresa não encontrada")
            return JSONResponse({"detail": "Empresa deletada com sucesso!"}, 200)
        except Exception as E:
            error_message(E)
