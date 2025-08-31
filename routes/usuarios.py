import json
from datetime import datetime
from typing import List

from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse

from database.db import Database
from database.models import Usuarios
from schemas.usuarios import GetUsuario, SetUsuario
from utils import error_message, fernet_crypt_info, hash_password


class UsuariosRouter(APIRouter):

    def __init__(self):
        super().__init__(prefix="/usuarios", tags=["Usuarios"])

        self.add_api_route('',
                           self.get_usuarios,
                           methods=['GET'],
                           status_code=200,
                           response_model=List[GetUsuario])

        self.add_api_route('/{id_usuario}',
                           self.get_usuario_by_id,
                           methods=['GET'],
                           response_model=GetUsuario,
                           status_code=200)

        self.add_api_route('',
                           self.set_usuario,
                           methods=['POST'],
                           response_model=SetUsuario,
                           status_code=201)

        self.add_api_route('',
                           self.patch_usuario,
                           methods=['PATCH'],
                           response_model=SetUsuario,
                           response_model_exclude={'cpf', 'senha'},
                           status_code=200)

        self.add_api_route('/{id_usuario}',
                           self.delete_usuario,
                           methods=['DELETE'],
                           status_code=200)

    def get_usuarios(self,
                     ativo: int = Query(
                         1, alias="ativo", description="Se o usuário estiver ativo ou não"),
                     pagina: int = Query(
                         1, alias="pagina", description="Número da página", gt=0),
                     limite: int = Query(
                         10, alias="limite", description="Número de registros por página", gt=0),
                     ):
        try:
            with Database() as db:
                db_usuarios = db.query(Usuarios).filter_by(
                    ativo=ativo).offset((pagina - 1) * limite).limit(limite)
                db_usuarios = db_usuarios.all()
                model_usuarios = [GetUsuario.model_validate(
                    db_usuario).model_dump() for db_usuario in db_usuarios]

            return JSONResponse(json.loads(json.dumps(model_usuarios, default=str)), 200)
        except Exception as E:
            error_message(E)

    def get_usuario_by_id(self, id_usuario: int = Path(..., gt=0)):
        try:
            with Database() as db:
                db_usuario = db.query(Usuarios).get(id_usuario)
                model_usuario = GetUsuario.model_validate(
                    db_usuario).model_dump()
            return JSONResponse(json.loads(json.dumps(model_usuario, default=str)), 200)
        except Exception as E:
            error_message(E)

    def set_usuario(self, usuario_info: SetUsuario = Body(default=SetUsuario().model_dump(exclude={'id_usuario'}))):
        try:
            usuario_info.senha = hash_password(usuario_info.senha)
            usuario_info.cpf = usuario_info.cpf.replace(
                '.', '').replace('-', '')
            usuario_info.cpf = fernet_crypt_info(usuario_info.cpf)
            with Database() as db:
                db_usuario = Usuarios(
                    **usuario_info.model_dump(exclude={'id_usuario'}))
                db.add(db_usuario)
                db.flush()
                db.refresh(db_usuario)
                model_usuario = GetUsuario.model_validate(
                    db_usuario).model_dump(mode='json')
                db.commit()
            return JSONResponse(model_usuario, 201)
        except Exception as E:
            error_message(E)

    def patch_usuario(self, usuario_info: SetUsuario = Body(default=SetUsuario().model_dump(exclude={'senha'})), id_usuario: int = Path(..., gt=0)):
        try:
            with Database() as db:
                db_usuario = db.query(Usuarios).get(id_usuario)
                for key, value in usuario_info.model_dump().items():
                    setattr(db_usuario, key, value)
                db.commit()
                model_usuario = GetUsuario.model_validate(
                    db_usuario).model_dump()
            return JSONResponse(model_usuario, 200)
        except Exception as E:
            error_message(E)

    def delete_usuario(self, id_usuario: int = Path(..., gt=0)):
        try:
            with Database() as db:
                db_usuario = db.query(Usuarios).filter(
                    Usuarios.id_usuario == id_usuario).update({'ativo': 2})
                db.commit()
            return JSONResponse({"detail": "Usuário deletado com sucesso!"}, 200)
        except Exception as E:
            error_message(E)
