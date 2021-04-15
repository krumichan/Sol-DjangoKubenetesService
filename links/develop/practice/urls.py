from django.urls import path
from . import views


urlpatterns = [
    path('ssh-command-execute-test', views.ssh_command_execute_test)
    , path('create-cluster-test', views.create_cluster_test)
    , path('delete-cluster-test', views.delete_cluster_test)
    , path('snapshot-cluster-test', views.snapshot_cluster_test)
    , path('restore-snapshot-cluster-test', views.restore_snapshot_cluster_test)
    , path('node-run-cluster-test', views.node_run_cluster_test)
    , path('rotate-certificates-cluster-test', views.rotate_certificates_cluster_test)
    , path('save-as-rke-templates-cluster-test', views.save_as_rke_templates_cluster_test)
    , path('run-cis-scan-cluster-test', views.run_cis_scan_cluster_test)
    ,
]
