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
    path('', views.validate, x("list_catalogs", "CatalogsMapper"))
    , path('list', views.validate,  x("list_catalogs", "CatalogsMapper"))

    # create
    # TODO: create form page 구현 필요.
    # , path('add', views.validate,  x("create_form_catalog", "CatalogsMapper"))
    # , path('add-form', views.validate,  x("create_form_catalog", "CatalogsMapper"))
    # , path('create', views.validate,  x("create_form_catalog", "CatalogsMapper"))
    # , path('create-form', views.validate,  x("create_form_catalog", "CatalogsMapper"))

    # clone
    # TODO: clone form page 구현 필요.
    # , path('<str:name>/copy', views.validate,  x("clone_form_catalog", "CatalogsMapper"))
    # , path('<str:name>/copy-form', views.validate,  x("clone_form_catalog", "CatalogsMapper"))
    # , path('<str:name>/clone', views.validate,  x("clone_form_catalog", "CatalogsMapper"))
    # , path('<str:name>/clone-form', views.validate,  x("clone_form_catalog", "CatalogsMapper"))

    # upgrade
    # TODO: upgrade form page 구현 필요.
    # , path('<str:name>/edit', views.validate,  x("upgrade_form_catalog", "CatalogsMapper"))
    # , path('<str:name>/edit-form', views.validate,  x("upgrade_form_catalog", "CatalogsMapper"))
    # , path('<str:name>/upgrade', views.validate,  x("upgrade_form_catalog", "CatalogsMapper"))
    # , path('<str:name>/upgrade-form', views.validate,  x("upgrade_form_catalog", "CatalogsMapper"))

    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    , path('api/clone', views.validate,  x("clone_catalog", "CatalogsMapper"))
    , path('api/create', views.validate,  x("create_catalog", "CatalogsMapper"))
    , path('api/upgrade', views.validate,  x("upgrade_catalog", "CatalogsMapper"))

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    # TODO: 모든 refresh API 구현 필요.
    # , path('refresh', views.validate,  x("refresh_catalogs", "CatalogsMapper"))
    # TODO: group refresh API 구현 필요.
    # group refresh 지원 ( wildcard:&, ex> aa&bb&cc/refresh )
    # , path('<str:names>/refresh', views.validate,  x("refresh_catalogs", "CatalogsMapper"))
    # TODO: group delete API 구현 필요.
    # group delete 지원 ( wildcard:&, ex> aa&bb&cc/delete )
    # , path('<str:names>/delete', views.validate,  x("delete_catalogs", "CatalogsMapper"))
    # TODO: enabled API 구현 필요.
    # group enabled 지원 ( wildcard:&, ex> aa&bb&cc/enabled )
    # , path('<str:names>/enabled', views.validate,  x("enabled_catalogs", "CatalogsMapper"))
    # TODO: search API 구현 필요.
    # , path('<str:search>/serach', views.validate,  x("serach_catalog", "CatalogsMapper"))

    #################################################


    #################################################
    # ajax support
    #################################################

    , path('ajax/getSpecificRowByName', views.validate, x("get_specific_row_by_name", "CatalogsMapper"))

    #################################################

]
