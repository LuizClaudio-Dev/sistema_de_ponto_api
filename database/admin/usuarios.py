from sqladmin import ModelView

from database.models.usuarios import Usuarios


class UsuariosAdmin(ModelView):
    model = Usuarios
    identity = "usuarios"
    '''Admin view for Usuarios model'''
    pk_columns = [Usuarios.id_usuario]
    can_create = True
    can_edit = True
    can_delete = True
    icon = "fa-solid fa-users"
    name = "Usuários"
    name_plural = "Usuários"
    column_list = [Usuarios.id_usuario, Usuarios.nome, Usuarios.email, Usuarios.cpf]
    form_columns = [Usuarios.nome, Usuarios.cpf, Usuarios.pis, Usuarios.email, Usuarios.senha]
    column_searchable_list = [Usuarios.nome, Usuarios.cpf, Usuarios.email]
    column_exclude_list = ["ativo", "motivo",
                           "data_criacao", "data_atualizacao"]
