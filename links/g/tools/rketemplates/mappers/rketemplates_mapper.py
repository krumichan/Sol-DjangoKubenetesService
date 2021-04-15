import json

from django.http import HttpRequest
from django.shortcuts import render, redirect

from common import constants as CC
from common.share import Share

from links.g.tools.rketemplates.services.rketemplates_service import RKETemplatesService


class RKETemplatesService:

    def __new__(cls):
        """
        새로운 instance 생성을 요청할 시, 자신이 소유하고 있는 instance를 반환한다.\n
        없을시, 새로 생성하여 반환한다.
        """

        if not hasattr(cls, "_me"):
            # instance 생성.
            cls._me = super(RKETemplatesService, cls).__new__(cls)
            # 해당 instance의 필수 요구 member 생성.
            cls._me.__share = Share()
            cls._me.__u_service = RKETemplatesService()
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

    def __forward(self, func_name, payload, html_name, js_name=""):

        # 자신의 instance를 임시로 변경.
        t = self._me

        # template 경로 및 context 설정.
        template = t.__share.generator_path(filepath=t.__filepath, file=html_name)
        context = {
            # web browser(template)에 뿌리기 위한 model 습득.
            CC.MODEL_STRING:
                t.__u_service.request_mapping(func_name=func_name, payload=payload)

            # web browser에 연동시킬 js file의 경로.
            , CC.JS_URL_STRING:
                "" if not js_name else t.__share.generator_path(filepath=t.__filepath, file=js_name)
        }

        return render(request=t.__request, template_name=template, context=context)

    def __redirect(self, func_name, payload, redirect_path):

        # 자신의 instance를 임시로 변경.
        t = self._me

        # service 실행.
        t.__u_service.request_mapping(func_name=func_name, payload=payload)

        return redirect(redirect_path)
