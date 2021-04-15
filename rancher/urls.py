from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),

    # global
    path('g/clusters/', include('links.g.clusters.urls')),
    path('g/multi-cluster-apps/', include('links.g.multiclusterapps.urls')),
    path('g/security/authentication/', include('links.g.security.authentication.urls')),
    path('g/security/globalroles/', include('links.g.security.globalroles.urls')),
    path('g/security/groups/', include('links.g.security.groups.urls')),
    path('g/security/policies/', include('links.g.security.policies.urls')),
    path('g/security/users/', include('links.g.security.users.urls')),
    path('g/settings/', include('links.g.settings.urls')),
    path('g/tools/catalogs/', include('links.g.tools.catalogs.urls')),
    path('g/tools/drivers/', include('links.g.tools.drivers.urls')),
    path('g/tools/rke-templates/', include('links.g.tools.rketemplates.urls')),

    # cluster
    path('c/<str:cluster_id>/persistent-volumes/', include('links.c.storage.persistentvolumes.urls')),
    path('c/<str:cluster_id>/storage-classes/', include('links.c.storage.storageclasses.urls')),

    # project


    # for test
    path('practice/', include('links.develop.practice.urls')),

]
