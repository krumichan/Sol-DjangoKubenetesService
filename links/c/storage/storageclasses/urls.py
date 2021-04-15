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
    path('', views.validate, x("list_storage_classes", "StorageClassesMapper"))
    , path('list', views.validate, x("list_storage_classes", "StorageClassesMapper"))

    # create form
    , path('add', views.validate, x("add_form_storage_class", "StorageClassesMapper"))
    , path('add-form', views.validate, x("add_form_storage_class", "StorageClassesMapper"))
    , path('create', views.validate, x("add_form_storage_class", "StorageClassesMapper"))
    , path('create-form', views.validate, x("add_form_storage_class", "StorageClassesMapper"))

    # detail
    , path('<str:name>/detail/', views.validate, x("detail_storage_class", "StorageClassesMapper"))

    # edit form
    # TODO: edit Page 구현 필요.
    # , path('<str:name>/edit', views.validate, x("list_storage_classes", "StorageClassesMapper"))
    # , path('<str:name>/edit-form', views.validate, x("list_storage_classes", "StorageClassesMapper"))

    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    , path('api/create', views.validate, x("add_storage_class", "StorageClassesMapper"))
    # TODO: edit API 구현 필요.
    # , path('api/edit', views.validate, x("edit_storage_class", "StorageClassesMapper"))

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    # TODO: delete API 구현 필요.
    # group delete 지원 ( wildcard:&, ex> aa&&bb&&cc/delete )
    # , path('<str:names>/delete', views.validate, x("delete_storage_classes", "StorageClassesMapper"))

    #################################################


    #################################################
    # ajax support
    #################################################

    , path('provisioner/<str:name>/', views.validate, x("load_provisioner", "StorageClassesMapper"))
    , path('ajax/loadProvisioner', views.validate, x("load_provisioner", "StorageClassesMapper"))
    ,

    #################################################
]
