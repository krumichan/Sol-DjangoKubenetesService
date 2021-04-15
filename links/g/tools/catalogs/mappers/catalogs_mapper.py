import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from common import constants as CC
from common.share import Share

from links.g.tools.catalogs.services.catalogs_service import CatalogsService


class CatalogsMapper:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, "_me"):
            # instance 생성.
            cls._me = super(CatalogsMapper, cls).__new__(cls)
            # 해당 instance의 필수 요구 member 생성.
            cls._me.__share = Share()
            cls._me.__c_service = CatalogsService()
            # 해당 instance의 필수 요구 변수를 생성.
            cls._me.__request = None
            cls._me.__filepath = None

        return cls._me

    def api_mapping(self, request, api_name, filepath, arguments):
        # TODO: 각종 검증 수행.

        # 인수로 받은 request가 HttpRequest 인지 확인.
        if not isinstance(request, HttpRequest):
            raise(self._me.__class__.__name__ + " object require for HttpRequest type object.")

        # 받은 api 이름을 protected 이름으로 변경.
        prot_name = "_" + api_name
        if not hasattr(self._me, prot_name):
            raise Exception(self._me.__class__.__name__ + " object has no attribute '" + api_name + "'")

        # protected 처리된 api function을 호출.
        reflect_func = getattr(self._me, prot_name)

        # 해당 instance의 member 변수 설정.
        self._me.__request = request
        self._me.__filepath = filepath

        return reflect_func(**arguments)

    def _list_catalogs(self, **arguments):
        """
        모든 Catalog Data 를 습득하여 View에 던진다.\n
        :param arguments: Client로부터 넘어온 각종 정보.
        :return: 요청을 출력할 View와 그 View에서 사용할 data
        """

        payload = {
            CC.OPTIONS_STRING: {
                "me": "true"
            }
        }

        return self._me.__forward(
            func_name="list_catalogs"
            , payload=payload
            , html_name="index.html"
            , js_name="index.js"
        )

    def _get_specific_row_by_name(self, **arguments):
        """
        특정 Catalog Name을 통하여 그 Name에 맞는 Catalog를 습득한다.\n
        :param arguments: Client로부터 넘어온 각종 정보.
        :return: 습득한 Catalog Row
        """

        # POST로 넘어온 body (bytes)를 string으로 변환
        body_string = self._me.__request.body.decode('utf-8')

        # string으로 변환한 body (string)을 json (dictionary) 로 변환
        body_data = json.loads(body_string)

        # dictinary로부터 검색에 사용할 Catalog의 name 습득
        name = body_data['name']

        if not name:
            raise Exception("Required 'name' attribute.")

        # name 이 None 값이 나올 경우는 coding miss를 제외하고는 사실상 없음.
        payload = {'name': name, 'me': 'true'}

        # catalog list 를 가공하여 습득.
        models = self._me.__c_service.request_mapping(
            func_name="list_catalogs", payload=payload
        )

        # name 값은 사실상 원자적인 data이기 때문에 Catalog List의 길이는 필시 1이 된다.
        # 그 Catalog List에서 하나밖에 없는 Catalog를 추출하여 던진다.
        return HttpResponse(json.dumps({"data": models[0]}), content_type="application/json")

    def _delete_Catalogs(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("catalog_data"))
        }

        return self._me.__redirect(
            func_name="delete_catalogs"
            , payload=payload
            , redirect_path="/g/tools/catalogs"
        )

    def _create_catalog(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("catalog_data"))
        }

        return self._me.__redirect(
            func_name="create_catalog"
            , payload=payload
            , redirect_path="/g/tools/catalogs"
        )

    def _upgrade_catalog(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("catalog_data"))
        }

        return self._me.__redirect(
            func_name="edit_catalog"
            , payload=payload
            , redirect_path="/g/tools/catalogs"
        )

    def _clone_catalog(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("catalog_data"))
        }

        return self._me.__redirect(
            func_name="clone_catalog"
            , payload=payload
            , redirect_path="/g/tools/catalogs"
        )

    def _delete_catalog(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("catalog_data"))
        }

        return self._me.__redirect(
            func_name="delete_catalog"
            , payload=payload
            , redirect_path="/g/tools/catalogs"
        )

    def _enabled_catalog(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("catalog_data"))
        }

        return self._me.__redirect(
            func_name="enabled_catalog"
            , payload=payload
            , redirect_path="/g/tools/catalogs"
        )

    def _refresh_catalog(self, **arguments):
        payload = {
            CC.OPTIONS_STRING: json.loads(self._me.__request.POST.get("catalog_data"))
        }

        return self._me.__redirect(
            func_name="refresh_catalog"
            , payload=payload
            , redirect_path="/g/tools/catalogs"
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
