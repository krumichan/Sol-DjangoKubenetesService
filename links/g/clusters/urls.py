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
    # TODO: list page 구현 필요.
    # path("", views.validate, x("list_clusters", "ClustersMapper"))
    # , path("list", views.validate, x("list_clusters", "ClustersMapper"))

    # select
    # TODO: select form page 구현 필요.
    # , path("add", views.validate, x("select_form_cluster", "SelectMapper"))
    # , path("add-form", views.validate, x("select_form_cluster", "SelectMapper"))
    # , path("create", views.validate, x("select_form_cluster", "SelectMapper"))
    # , path("create-form", views.validate, x("select_form_cluster", "SelectMapper"))

    # create ( name = cluster type )
    # TODO: create form page 구현 필요.
    # , path("add/<str:name>", views.validate, x("create_form_cluster", "CreateMapper"))
    # , path("add-form/<str:name>", views.validate, x("create_form_cluster", "CreateMapper"))
    # , path("create/<str:name>", views.validate, x("create_form_cluster", "CreateMapper"))
    # , path("create-form/<str:name>", views.validate, x("create_form_cluster", "CreateMapper"))

    # node run ( name = cluster name )
    # , path("<str:name>/node-run", views.validate, x("node_run_form_cluster", "NodeRunMapper"))

    # restore snapshot
    # TODO: restore snapshot form 구현 필요.
    # snapshot location sample : https://10.0.0.165/v3/clusters/c-w5q8c/etcdbackups
    # , path('<str:name>/restore-snapshot', views.validate, x("restore_snapshot_form_cluster", "ClustersMapper"))
    # , path('<str:name>/restore-snapshot-form', views.validate, x("restore_snapshot_form_cluster", "ClustersMapper"))

    # rotate certificates
    # TODO: rotate certificates form 구현 필요.
    # , path('<str:name>/rotate-certificates', views.validate, x("rotate_certificates_form_cluster", "ClustersMapper"))
    # , path('<str:name>/rotate-certificates-form', views.validate, x("rotate_certificates_form_cluster", "ClustersMapper"))

    # run CIS scan
    # TODO: run CIS scan form 구현 필요.
    # , path('<str:name>/run-cis-scan', views.validate, x("run_cis_scan_form_cluster", "ClustersMapper"))
    # , path('<str:name>/run-cis-scan-form', views.validate, x("run_cis_scan_form_cluster", "ClustersMapper"))

    # save as RKE templates
    # TODO: save as RKE templates form 구현 필요.
    # , path('<str:name>/save-as-rke-templates', views.validate, x("save_as_rke_templates_form_cluster", "ClustersMapper"))
    # , path('<str:name>/save-as-rke-templates-form', views.validate, x("save_as_rke_templates_form_cluster", "ClustersMapper"))

    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    # ( cluster가 active 상태가 아니어도 가능 )
    path('api/create', views.validate, x("create_existing_cluster", "CreateMapper"))
    , path('api/restore-snapshot', views.validate, x("restore_snapshot_cluster", "ClustersMapper"))
    , path('api/node-run', views.validate, x("node_run_cluster", "NodeRunMapper"))
    , path('api/rotate-certificates', views.validate, x("rotate_certificates_cluster", "ClustersMapper"))

    # TODO: cluster api 구현 필요.
    , path('api/run-cis-scan', views.validate, x("run_cis_scan_cluster", "ClustersMapper"))
    , path('api/save-as-rke-templates', views.validate, x("save_as_rke_templates_cluster", "ClustersMapper"))

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    # group delete 지원 ( wildcard:&, ex> aa&bb&cc/delete )
    , path('<str:names>/delete', views.validate, x("delete_clusters", "ClustersMapper"))
    # group snapshot now 지원 ( wildcard:&, ex> aa&bb&cc/snapshot-now )
    , path('<str:names>/snapshot-now', views.validate, x("snapshot_now_clusters", "ClustersMapper"))
    # TODO: search API 구현 필요.
    # , path('<str:search>/search', views.validate, x("search_cluster", "ClustersMapper"))

    #################################################


    #################################################
    # ajax support
    #################################################

    #################################################
]