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
    # path('', views.validate, x("list_users", "UsersMapper"))
    # , path('list', views.validate, x("list_users", "UsersMapper"))

    # create
    # TODO: create form 구현 필요.
    # , path("add", views.validate, x("create_form_user", "CreateMapper"))
    # , path("add-form", views.validate, x("create_form_user", "CreateMapper"))
    # , path("create", views.validate, x("create_form_user", "CreateMapper"))
    # , path("create-form", views.validate, x("create_form_user", "CreateMapper"))

    # upgrade
    # TODO: upgrade form 구현 필요.
    # , path("edit", views.validate, x("edit_form_user", "CreateMapper"))
    # , path("edit-form", views.validate, x("edit_form_user", "CreateMapper"))
    # , path("upgrade", views.validate, x("edit_form_user", "CreateMapper"))
    # , path("upgrade-form", views.validate, x("edit_form_user", "CreateMapper"))

    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    # TODO: create API 구현 필요.
    # , path("api/create", views.validate, x("create_user", "CreateMapper"))
    # TODO: edit API 구현 필요.
    # , path("api/edit", views.validate, x("edit_user", "CreateMapper"))

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    # TODO: group activate 구현 필요.
    # group activate 지원 ( wildcard:&, ex> aa&bb&cc/activate )
    # , path("<str:names>/actiavte", views.validate, x("activate_users", "UsersMapper"))
    # TODO: group deactivate 구현 필요.
    # group deactivate 지원 ( wildcard:&, ex> aa&bb&cc/activate )
    # , path("<str:names>/deactivate", views.validate, x("deactivate_users", "UsersMapper"))
    # TODO: group delete 구현 필요.
    # group delete 지원 ( wildcard:&, ex> aa&bb&cc/delete )
    # , path("<str:names>/delete", views.validate, x("delete_users", "UsersMapper"))
    # TODO: refresh 구현 필요.
    # , path("refresh", views.validate, x("refresh_users", "UsersMapper"))
    # TODO: serach 구현 필요.
    # , path('<str:search>/search', views.validate, x("search_user", "UsersMapper"))

    #################################################


    #################################################
    # ajax support
    #################################################

    #################################################
]