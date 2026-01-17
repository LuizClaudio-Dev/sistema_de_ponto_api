from sqladmin import ModelView

from database.models.empresas import Empresas


class EmpresasAdmin(ModelView):
    model = Empresas
    identity = "empresas"
    '''Admin view for Empresas model'''
    pk_columns = [Empresas.id_empresa]
    can_create = True
    can_edit = True
    can_delete = True
    icon = "fa-solid fa-building"
    name = "Empresas"
    name_plural = "Empresas"
    column_list = [Empresas.id_empresa, Empresas.nome_fantasia, Empresas.cnpj]
    form_columns = [Empresas.nome_fantasia, Empresas.cnpj, Empresas.razao_social,
                    Empresas.cep, Empresas.logradouro, Empresas.complemento, Empresas.numero,
                    Empresas.bairro, Empresas.cidade, Empresas.uf]
    column_searchable_list = [Empresas.nome_fantasia, Empresas.cnpj]
    column_exclude_list = ["ativo", "motivo",
                           "data_criacao", "data_atualizacao"]
