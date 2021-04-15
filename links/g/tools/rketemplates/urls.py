from django.urls import path
from . import views


def x(c, m):
    return {
        "callback": c
        , "mapper": m
    }


urlpatterns = [
    #################################################
    # web browser 접근 가능 URL ( 즉, Client 접근 가능 )
    #################################################
    # listing
    # TODO: listing 구현 필요.
    # path('', views.validate, x("list_rketemplates", "RKETemplatesMapper"))
    # , path('list', views.validate, x("list_rketemplates", "RKETemplatesMapper"))

    # create template
    # TODO: create template form 구현 필요.
    # , path("add", views.validate, x("create_form_rketemplate", "CreateRKETemplateMapper"))
    # , path("add-form", views.validate, x("create_form_rketemplate", "CreateRKETemplateMapper"))
    # , path("create", views.validate, x("create_form_rketemplate", "CreateRKETemplateMapper"))
    # , path("create-form", views.validate, x("create_form_rketemplate", "CreateRKETemplateMapper"))

    # create revision
    # TODO: create revision form 구현 필요.
    # , path("<str:name>/revision/add", x("create_form_revision", "CreateRKETemplateMapper"))
    # , path("<str:name>/revision/add-form", x("create_form_revision", "CreateRKETemplateMapper"))
    # , path("<str:name>/revision/create", x("create_form_revision", "CreateRKETemplateMapper"))
    # , path("<str:name>/revision/create-form", x("create_form_revision", "CreateRKETemplateMapper"))

    # upgrade
    # TODO: upgrade form 구현 필요.
    # , path("edit", views.validate, x("edit_form_rketemplate", "CreateRKETemplateMapper"))
    # , path("edit-form", views.validate, x("edit_form_rketemplate", "CreateRKETemplateMapper"))
    # , path("upgrade", views.validate, x("edit_form_rketemplate", "CreateRKETemplateMapper"))
    # , path("upgrade-form", views.validate, x("edit_form_rketemplate", "CreateRKETemplateMapper"))
    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################
    # TODO: clone API 구현 필요.
    # , path("api/clone", views.validate, x("clone_rketemplate", "CreateRKETemplateMapper"))
    # TODO: create API 구현 필요.
    # , path("api/create", views.validate, x("create_rketemplate", "CreateRKETemplateMapper"))
    # TODO: edit API 구현 필요.
    # , path("api/edit", views.validate, x("edit_rketemplate", "CreateRKETemplateMapper"))
    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################
    # TODO: disable 구현 필요.
    # group disable 지원 ( wildcard:&, ex> aa&bb&cc/disable )
    # , path("<str:name>/revision/<str:names>/disable", views.validate, x("disable_rketemplate", "RKETemplatesMapper"))
    # TODO: enable 구현 필요.
    # group enable 지원 ( wildcard:&, ex> aa&bb&cc/enable )
    # , path("<str:name>/revision/<str:names>/enable", views.validate, x("enable_rketemplate", "RKETemplatesMapper"))
    # TODO: rke template group delete 구현 필요.
    # rke template group delete 지원 ( wildcard:&, ex> aa&bb&cc/delete )
    # , path("<str:names>/delete", views.validate, x("delete_rketemplate", "RKETemplatesMapper"))
    # TODO: revision group delete 구현 필요.
    # rke template group delete 지원 ( wildcard:&, ex> aa&bb&cc/delete )
    # , path("<str:name>/revision/<str:names>/delete", views.validate, x("delete_revisions", "RKETemplatesMapper"))
    # TODO: serach 구현 필요.
    # , path('<str:search>/search', views.validate, x("search_rketemplate", "RKETemplatesMapper"))
    # TODO: set default 구현 필요.
    # , path("<str:name>/revision/<str:names>/default", views.validate, x("set_default_rketemplate", "RKETemplatesMapper"))
    #################################################


    #################################################
    # ajax support
    #################################################

    #################################################
]