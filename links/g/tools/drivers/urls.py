from django.urls import path
from . import views


def x(c, m):
    return {
        "callback": c
        , "mapper": m
    }


cluster_patterns = [
    #################################################
    # web browser 접근 가능 URL ( 즉, Client 접근 가능 )
    #################################################

    # listing
    # TODO: listing 구현 필요.
    # path('', views.validate, x("list_cluster_drivers", "ClusterMapper"))
    # , path('list', views.validate, x("list_cluster_drivers", "ClusterMapper"))
    # , path('cluster', views.validate, x("list_cluster_drivers", "ClusterMapper"))
    # , path('cluster/list', views.validate, x("list_cluster_drivers", "ClusterMapper"))

    # create
    # TODO: create form 구현 필요.
    # , path("cluster/add", views.validate, x("create_form_cluster_driver", "CreateClusterMapper"))
    # , path("cluster/add-form", views.validate, x("create_form_cluster_driver", "CreateClusterMapper"))
    # , path("cluster/create", views.validate, x("create_form_cluster_driver", "CreateClusterMapper"))
    # , path("cluster/create-form", views.validate, x("create_form_cluster_driver", "CreateClusterMapper"))

    # upgrade
    # TODO: upgrade form 구현 필요.
    # , path("cluster/edit", views.validate, x("edit_form_driver", "CreateClusterMapper"))
    # , path("cluster/edit-form", views.validate, x("edit_form_driver", "CreateClusterMapper"))
    # , path("cluster/upgrade", views.validate, x("edit_form_driver", "CreateClusterMapper"))
    # , path("cluster/upgrade-form", views.validate, x("edit_form_driver", "CreateClusterMapper"))

    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    # TODO: create API 구현 필요.
    # , path("api/cluster/create", views.validate, x("create_cluster_driver", "CreateClusterMapper"))
    # TODO: edit API 구현 필요.
    # , path("api/cluster/edit", views.validate, x("edit_cluster_driver", "CreateClusterMapper"))

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    # TODO: group activate 구현 필요.
    # group activate 지원 ( wildcard:&, ex> aa&bb&cc/activate )
    # , path("cluster/<str:names>/actiavte", views.validate, x("activate_cluster_drivers", "ClusterMapper"))
    # TODO: group deactivate 구현 필요.
    # group deactivate 지원 ( wildcard:&, ex> aa&bb&cc/activate )
    # , path("cluster/<str:names>/deactivate", views.validate, x("deactivate_cluster_drivers", "ClusterMapper"))
    # TODO: group delete 구현 필요.
    # group delete 지원 ( wildcard:&, ex> aa&bb&cc/delete )
    # , path("cluster/<str:names>/delete", views.validate, x("delete_cluster_drivers", "ClusterMapper"))
    # TODO: refresh 구현 필요.
    # , path("cluster/refresh", views.validate, x("refresh_cluster_drivers", "ClusterMapper"))
    # TODO: serach 구현 필요.
    # , path('cluster/<str:search>/search', views.validate, x("search_cluster_drivers", "ClusterMapper"))

    #################################################


    #################################################
    # ajax support
    #################################################

    #################################################
]


node_patterns = [
    #################################################
    # web browser 접근 가능 URL ( 즉, Client 접근 가능 )
    #################################################

    # listing
    # TODO: listing 구현 필요.
    # path('node', views.validate, x("list_node_drivers", "NodeMapper"))
    # , path('node/list', views.validate, x("list_node_drivers", "NodeMapper"))

    # create
    # TODO: create form 구현 필요.
    # , path("node/add", views.validate, x("create_form_node_driver", "CreateNodeMapper"))
    # , path("node/add-form", views.validate, x("create_form_node_driver", "CreateNodeMapper"))
    # , path("node/create", views.validate, x("create_form_node_driver", "CreateNodeMapper"))
    # , path("node/create-form", views.validate, x("create_form_node_driver", "CreateNodeMapper"))

    # upgrade
    # TODO: upgrade form 구현 필요.
    # , path("node/edit", views.validate, x("edit_form_node_driver", "CreateNodeMapper"))
    # , path("node/edit-form", views.validate, x("edit_form_node_driver", "CreateNodeMapper"))
    # , path("node/upgrade", views.validate, x("edit_form_node_driver", "CreateNodeMapper"))
    # , path("node/upgrade-form", views.validate, x("edit_form_node_driver", "CreateNodeMapper"))

    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    # TODO: create API 구현 필요.
    # , path("api/node/create", views.validate, x("create_node_driver", "CreateNodeMapper"))
    # TODO: edit API 구현 필요.
    # , path("api/node/edit", views.validate, x("edit_node_driver", "CreateNodeMapper"))

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    # TODO: group activate 구현 필요.
    # group activate 지원 ( wildcard:&, ex> aa&bb&cc/activate )
    # , path("node/<str:names>/actiavte", views.validate, x("activate_node_drivers", "NodeMapper"))
    # TODO: group deactivate 구현 필요.
    # group deactivate 지원 ( wildcard:&, ex> aa&bb&cc/activate )
    # , path("node/<str:names>/deactivate", views.validate, x("deactivate_node_drivers", "NodeMapper"))
    # TODO: group delete 구현 필요.
    # group delete 지원 ( wildcard:&, ex> aa&bb&cc/delete )
    # , path("node/<str:names>/delete", views.validate, x("delete_node_drivers", "NodeMapper"))
    # TODO: serach 구현 필요.
    # , path('node/<str:search>/search', views.validate, x("search_node_drivers", "NodeMapper"))

    #################################################


    #################################################
    # ajax support
    #################################################

    #################################################
]


urlpatterns = cluster_patterns + node_patterns
