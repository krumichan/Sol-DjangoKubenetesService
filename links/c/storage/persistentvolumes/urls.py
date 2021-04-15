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
    path('', views.validate, x("list_persistent_volumes", "PersistentVolumesMapper"))
    , path('list', views.validate, x("list_persistent_volumes", "PersistentVolumesMapper"))

    # create form
    , path('add', views.validate, x("add_form_persistent_volume", "PersistentVolumesMapper"))
    , path('add-form', views.validate, x("add_form_persistent_volume", "PersistentVolumesMapper"))
    , path('create', views.validate, x("add_form_persistent_volume", "PersistentVolumesMapper"))
    , path('create-form', views.validate, x("add_form_persistent_volume", "PersistentVolumesMapper"))

    # detail
    , path('<str:name>/detail', views.validate, x("detail_persistent_volume", "PersistentVolumesMapper"))

    # edit form
    # TODO: edit Page 구현 필요.
    # , path('<str:name>/edit', views.validate, g("edit_persistent_volume", "PersistentVolumesMapper"))
    # , path('<str:name>/edit-form', views.validate, g("edit_persistent_volume", "PersistentVolumesMapper"))

    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    , path('api/create', views.validate, x("add_persistent_volume", "PersistentVolumesMapper"))
    # TODO: edit API 구현 필요.
    # , path('api/edit', views.validate, g("edit_persistent_volume", "PersistentVolumesMapper"))

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    # TODO: delete API 구현 필요.
    # group delete 지원 ( wildcard:&, ex> aa&&bb&&cc/delete )
    # , path('<str:names>/delete', views.validate, g("delete_persistent_volumes", "PersistentVolumesMapper"))

    #################################################


    #################################################
    # ajax support
    #################################################



    #################################################
]
