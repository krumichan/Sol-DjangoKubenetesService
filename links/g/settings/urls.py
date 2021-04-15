from django.urls import path
from . import views


def x(c, m):
    return {
        "callback": c
        , "mapper": m
    }


advanced_patterns = [
    #################################################
    # web browser 접근 가능 URL ( 즉, Client 접근 가능 )
    #################################################
    # viewing
    # TODO: viewing 구현 필요.
    # path('', views.validate, x("view_advanced_settings", "AdvancedSettingsMapper"))

    # upgrade
    # TODO: upgrade form 구현 필요.
    # , path("edit", views.validate, x("edit_form_advanced_settings", "EditAdvacnedSettingsMapper"))
    # , path("edit-form", views.validate, x("edit_form_advanced_settings", "EditAdvacnedSettingsMapper"))
    # , path("upgrade", views.validate, x("edit_form_advanced_settings", "EditAdvacnedSettingsMapper"))
    # , path("upgrade-form", views.validate, x("edit_form_advanced_settings", "EditAdvacnedSettingsMapper"))
    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################
    # TODO: edit API 구현 필요.
    # , path("api/edit", views.validate, x("edit_advanced_settings", "EditAdvacnedSettingsMapper"))
    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################

    #################################################


    #################################################
    # ajax support
    #################################################

    #################################################
]

feture_patterns = [
    #################################################
    # web browser 접근 가능 URL ( 즉, Client 접근 가능 )
    #################################################
    # listing
    # TODO: listing 구현 필요.
    # path('feture-flags', views.validate, x("list_feture_flags", "FetureFlagsMapper"))
    # , path('feture-flags/list', views.validate, x("list_feture_flags", "FetureFlagsMapper"))
    #################################################


    #################################################
    # web browser 접근 불가 API ( 즉, Client 접근 불가 )
    #################################################

    #################################################


    #################################################
    # web browser 접근 가능 API ( 즉, Client 접근 가능 )
    #################################################
    # TODO: group activate 구현 필요.
    # group activate 지원 ( wildcard:&, ex> aa&bb&cc/activate )
    # , path("feture-flags/<str:names>/actiavte", views.validate, x("activate_feture_flags", "FetureFlagsMapper"))
    # TODO: group deactivate 구현 필요.
    # group deactivate 지원 ( wildcard:&, ex> aa&bb&cc/activate )
    # , path("feture-flags/<str:names>/deactivate", views.validate, x("deactivate_feture_flags", "FetureFlagsMapper"))
    # TODO: serach 구현 필요.
    # , path('feture-flags/<str:search>/search', views.validate, x("search_user", "FetureFlagsMapper"))
    #################################################


    #################################################
    # ajax support
    #################################################

    #################################################
]

urlpatterns = advanced_patterns + feture_patterns
