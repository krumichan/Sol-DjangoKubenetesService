from django.urls import path
from . import views


def x(c, m):
    return {
        "callback": c
        , "mapper": m
    }


mca_patterns = [
    #################################################
    # web browser 접근 가능 URL ( 즉, Client 접근 가능 )
    #################################################

    # listing
    path('', views.validate, x("list_multi_cluster_applications", "MultiClusterAppsMapper"))
    , path('list', views.validate, x("list_multi_cluster_applications", "MultiClusterAppsMapper"))

    # create
    # TODO: create form page 구현 필요.
    # , path('add', views.validate, x("create_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('add-form', views.validate, x("create_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('create', views.validate, x("create_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('create-form', views.validate, x("create_form_multi_cluster_application", "MultiClusterAppsMapper"))

    # clone
    # TODO: clone form page 구현 필요.
    # , path('<str:name>/copy', views.validate, x("clone_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('<str:name>/copy-form', views.validate, x("clone_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('<str:name>/clone', views.validate, x("clone_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('<str:name>/clone-form', views.validate, x("clone_form_multi_cluster_application", "MultiClusterAppsMapper"))

    # upgrade
    # TODO: upgrade form page 구현 필요.
    # , path('<str:name>/edit', views.validate, x("upgrade_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('<str:name>/edit-form', views.validate, x("upgrade_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('<str:name>/upgrade', views.validate, x("upgrade_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('<str:name>/upgrade-form', views.validate, x("upgrade_form_multi_cluster_application", "MultiClusterAppsMapper"))

    # rollback
    # TODO: rollback form page 구현 필요.
    # , path('<str:name>/revision', views.validate, x("rollback_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('<str:name>/revision-form', views.validate, x("rollback_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('<str:name>/rollback', views.validate, x("rollback_form_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('<str:name>/rollback-form', views.validate, x("rollback_form_multi_cluster_application", "MultiClusterAppsMapper"))

    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    # , path('api/clone', views.validate, x("clone_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('api/create', views.validate, x("create_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('api/delete', views.validate, x("delete_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('api/rollback', views.validate, x("rollback_multi_cluster_application", "MultiClusterAppsMapper"))
    # , path('api/upgrade', views.validate, x("upgrade_multi_cluster_application", "MultiClusterAppsMapper"))

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    # TODO: delete API 구현 필요.
    # group delete 지원 ( wildcard:&, ex> aa&&bb&&cc/delete )
    # , path('<str:names>/delete', views.validate, x("delete_multi_cluster_applications", "MultiClusterAppsMapper"))
    # TODO: search 구현 필요.
    # group search 지원 ( wildcard:&, ex> aa&&bb&&cc/search )
    # , path('<str:search>/search', views.validate, x("search_multi_cluster_application", "MultiClusterAppsMapper"))

    #################################################


    #################################################
    # ajax support
    #################################################

    #################################################
]

t_patterns = [
    #################################################
    # web browser 접근 가능 URL ( 즉, Client 접근 가능 )
    #################################################

    # listing
    path('templates', views.validate, x("list_templates", "TemplatesMapper"))
    , path('templates/list', views.validate, x("list_templates", "TemplatesMapper"))

    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    , path("templates/refresh", views.validate, x("refresh_templates", "TemplatesMapper"))
    , path("templates/<str:name>/category-filter", views.validate, x("filter_templates", "TemplatesMapper"))
    # TODO: serach 구현 필요.
    # group search 지원 ( wildcard:&, ex> aa&&bb&&cc/search )
    # , path('<search>/search', views.validate, x("search_template", "TemplatesMapper"))

    #################################################


    #################################################
    # ajax support
    #################################################

    #################################################
]


urlpatterns = mca_patterns + t_patterns
