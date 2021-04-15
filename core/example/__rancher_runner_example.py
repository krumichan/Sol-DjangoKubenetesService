import urllib3

from .__rancher_client_example import RancherClientExample

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RancherRunnerExample:
    """
    Rancher Client 를 제공하는 Rancher Client Template Example Class
    """

    ### static field ###

    # TODO: access_key 및 secret_key 를 web 시작과 함께 유동적으로 받아올 방법이 필요.
    # __default_url = 'https://10.0.0.154/v3'
    # __access_key = 'token-ltwmc'
    # __secret_key = '6xw6slm47zlnmkdhjmnmlxmsg7dtlmb46bnh5rpc8c6kzdpwf8q2fb'
    # __verify = False

    __default_url = 'https://10.0.0.165/v3'
    __access_key = 'token-sl6xh'
    __secret_key = '28jn8nnkvq9lz97psj2db58jrdlw6zq8msvhqclxdzbnls86qgv8s4'
    __verify = False

    __now_url = __default_url
    __now_url_type = "global"
    __now_type_id = ""

    __separator = "/"

    __cl = None

    ####################

    def is_xxxxx(self, url_type, type_id=""):
        """
        현재 Rancher Client의 url type이 기대하는 url type과 일치하는지 확인한다.\n
        :param url_type: 기대하는 url type.
        :param type_id: global 이외의 요구되는 cluster 또는 project id.
        :return: 일치 여부.
        """

        # 조건 확인 순서.
        # ① [필수And] 요청으로 온 URL 타입과 현객체의 URL 타입이 같은지 비교. ( 다를시 Schema 를 재호출 해야함. )
        # ② [임의Or]  요청으로 온 URL 타입이 global 인지 확인. ( global일 경우, id를 확인할 필요가 없음 )
        # ③ [임의Or]  요청으로 온 URL 타입이 global 이 아닌 경우, 요청의 id와 현객체의 id를 비교 ( 다를시 Schema 를 재호출 해야함. )

        return \
            url_type == self.__now_url_type and \
            (url_type == "global" or
             type_id == self.__now_type_id)

    def new_url_evaluate_then_reload_schema(self, url_type="global", type_id=""):
        """
        인수의 url type에 맞는 Schema를 생성한다.\n
        valid url = ["cluster", "projects", "global"], default="global"\n
        :param url_type: Rancher Client의 Schema를 구성하기 위한 url type
        :param type_id: Schema 재구성시 사용되는 id
        """

        # Rancher Client가 확립되어 있지 않으면 확립시킨다.
        self.__create_if_not_exists()

        # 실패할 때 rollback을 위하여 현재의 url을 보존한다.
        save_url = self.__now_url
        save_url_type = self.__now_url_type
        save_type_id = self.__now_type_id

        # 각 schema 종류에 따라 분류하여 새로운 schema를 확립한다.
        try:
            if url_type == "global":
                new_url = self.__default_url
            elif url_type in ["cluster", "project"]:
                new_url = self.__default_url + self.__separator + url_type + self.__separator + type_id

            # 부정한 type의 경우.
            else:
                raise TypeError("url type is invalid. check your url type." + "\n" + "url type:" + url_type)

            # 새로운 url에 대한 schema를 reload 한다.
            self.__cl.evaluate_url_then_reload_schema(new_url)
            self.__now_url = new_url
            self.__now_url_type = url_type
            self.__now_type_id = type_id

        # schema 확립시에 error가 발생하였을 경우.
        except Exception as e:
            # 이전의 schema로 rollback한다.
            self.__cl.evaluate_url_then_reload_schema(save_url)
            self.__now_url = save_url
            self.__now_url_type = save_url_type
            self.__now_type_id = save_type_id
            raise e

    def load_client(self):
        """
        Rancher Client 를 호출한다.\n
        만약 Rancher Client에 대한 호출이 처음이라면, Rancher Client를 생성한 뒤 호출하며,
        이전에 호출된 이후의 호출이라면, 기존의 Rancher Client를 반환한다.\n
        :return: RancherCore Class 가 소유하고 있는 Rancher Client
        """

        self.__create_if_not_exists()
        return self.__cl

    def __create_if_not_exists(self):
        """
        Client가 존재하지 않을 경우 Client를 생성한다.
        """

        if self.__cl is None:
            self.__cl = self.__client()
            print(" Create Client... ")

    def __client(self):
        """
        Rancher Client를 생성한 뒤 반환한다.\n
        :return: 생성된 Rancher Client
        """
        print("start getting rancher client exmaple...")

        cl = RancherClientExample(url=self.__default_url
                                  , access_key=self.__access_key
                                  , secret_key=self.__secret_key
                                  , verify=self.__verify)

        self.__now_url = self.__default_url
        self.__now_url_type = "global"

        print("success getting client...")

        return cl
