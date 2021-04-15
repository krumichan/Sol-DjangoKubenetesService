import json

from django.http import HttpRequest
from django.shortcuts import render, redirect

from common import constants as CC
from common.share import Share

from links.g.clusters.services.clusters_service import ClustersService


class ClustersMapper:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, "_me"):
            # instance 생성.
            cls._me = super(ClustersMapper, cls).__new__(cls)
            # 해당 instance의 필수 요구 member 생성.
            cls._me.__share = Share()
            cls._me.__c_service = ClustersService()
            # 해당 instance의 필수 요구 변수 생성.
            cls._me.__request = None
            cls._me.__filepath = None

        return cls._me

    def api_mapping(self, request, api_name, filepath, arguments):
        # TODO: 각종 검증 수행.

        # 인수로 받은 REQUEST가 HttpRequest 인지 확인.
        if not isinstance(request, HttpRequest):
            raise(self._me.__class__.__name__ + " object require for HttpRequest type object.")

        # 받은 api 이름을 protected 이름으로 변경.
        prot_name = "_" + api_name
        if not hasattr(self._me, prot_name):
            raise Exception(self._me.__class__.__name__ + " object has no attribte '" + api_name + "'")

        # protected 처리된 api function을 호출.
        reflect_func = getattr(self._me, prot_name)

        # 해당 instance의 member 변수 설정.
        self._me.__request = request
        self._me.__filepath = filepath

        return reflect_func(**arguments)

    def _delete_clusters(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: arguments
        }

        return self._me.__redirect(
            func_name="delete_clusters"
            , payload=payload
            , redirect_path="g/clusters"
        )

    def _restore_snapshot_cluster(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("clusterData"))
        }

        return self._me.__redirect(
            func_name="restore_snapshot_cluster"
            , payload=payload
            , redirect_path="/g/clusters"
        )

    def _snapshot_now_clusters(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: arguments
        }

        return self._me.__redirect(
            func_name="snapshot_now_clusters"
            , payload=payload
            , redirect_path="/g/clusters"
        )

    def _rotate_certificates_cluster(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("clusterData"))
        }

        return self._me.__redirect(
            func_name="rotate_certificates_cluster"
            , payload=payload
            , redirect_path="/g/clusters"
        )

    def _save_as_rke_templates_cluster(self, **arguments):
        cluster_data = json.loads(self._me.__request.POST.get("clusterData"))

        if CC.NAME_STRING not in cluster_data:
            raise Exception("Save as RKE Template API require cluster 'name' attribute.")

        name = cluster_data[CC.NAME_STRING]

        payload = {
            CC.OPTIONS_STRING: cluster_data
        }

        return self._me.__redirect(
            func_name="save_as_rke_templates_cluster"
            , payload=payload
            # TODO: clustername/<name> -> clustername으로 cluster를 찾고 그 안의 clusterTemplateRevisionId를 통해 redirect.
            , redirect_path="/g/tools/rke-templates/clustername/" + name
        )

    def _run_cis_scan_cluster(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("clusterData"))
        }

        return self._me.__redirect(
            func_name="run_cis_scan_cluster"
            , payload=payload
            , redirect_path="/g/clusters"
        )

    def __forward(self, func_name, payload, html_name, js_name=""):

        # 자신의 instance를 임시로 변경.
        t = self._me

        # template 경로 및 context 설정.
        template = t.__share.generator_path(filepath=t.__filepath, file=html_name)
        context = {
            # web browser(template)에 뿌리기 위한 model 습득.
            CC.MODEL_STRING:
                t.__c_service.request_mapping(func_name=func_name, payload=payload)

            # web browser에 연동시킬 js file의 경로.
            , CC.JS_URL_STRING:
                "" if not js_name else t.__share.generator_path(filepath=t.__filepath, file=js_name)
        }

        return render(request=t.__request, template_name=template, context=context)

    def __redirect(self, func_name, payload, redirect_path):

        # 자신의 instance를 임시로 변경.
        t = self._me

        # service 실행.
        t.__c_service.request_mapping(func_name=func_name, payload=payload)

        return redirect(redirect_path)
