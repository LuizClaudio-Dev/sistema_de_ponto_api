from sqladmin import ModelView

from database.models.empresas_usuarios_perfis import EmpresasUsuariosPerfis


class EmpresasUsuariosPerfisAdmin(ModelView):
    model = EmpresasUsuariosPerfis
    identity = "empresas_usuarios_perfis"
    '''Admin view for EmpresasUsuariosPerfis model'''
    pk_columns = [EmpresasUsuariosPerfis.id_empresa_usuario_perfil]
    can_create = True
    can_edit = True
    can_delete = True
    icon = "fa-solid fa-user-tag"
    name = "Empresa Usuário Perfil"
    name_plural = "Empresas Usuários Perfis"
    column_list = [EmpresasUsuariosPerfis.id_empresa_usuario_perfil, EmpresasUsuariosPerfis.empresa, EmpresasUsuariosPerfis.usuario, EmpresasUsuariosPerfis.perfil]
    form_columns = [EmpresasUsuariosPerfis.empresa, EmpresasUsuariosPerfis.usuario, EmpresasUsuariosPerfis.perfil]
    column_searchable_list = [EmpresasUsuariosPerfis.empresa, EmpresasUsuariosPerfis.usuario, EmpresasUsuariosPerfis.perfil]
    column_exclude_list = ["ativo", "motivo",
                           "data_criacao", "data_atualizacao"]
