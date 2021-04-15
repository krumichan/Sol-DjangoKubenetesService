import paramiko


class ClientSshError(Exception):
    pass


class SshClientSample:
    def __init__(self, server, username=None, password=None, port=22):
        """
        Ssh Client를 제공하기 위한 생성자이다.\n
        :param server: host 명.
        :param username: username.
        :param password: password.
        :param port: port.
        """

        self.__server = server
        self.__username = username
        self.__password = password
        self.__port = port

        self.__client = None
        # self.__sftp = None
        self.__is_opened = False

        self.__open_self(
            self.__server
            , self.__username
            , self.__password
            , self.__port
        )

    def __del__(self):
        """
        해당 instance의 client가 열려있는 경우, 제거한다.
        """

        try:
            self.close()
        except:
            pass

    def close(self):
        """
        해당 instance의 SSH Client를 close 한다.\n
        :return:
        """
        if not self.__check_client_exists():
            raise ClientSshError("Client doesn't exists.")

        else:
            self.__close_self()

    def execute(self, command):
        """
        명령어를 실행한다.\n
        list와 string만 지원한다.\n
        :param command: 실행시킬 command ( supported list, str )
        :return: 실행 결과인 stdin, stdout, stderr를 반환.
        """

        # command 검증. 실패시 error를 던짐.
        self.__check_command(command)

        # 명령어 실행
        return self.__client.exec_command(command)

        # stdin, stdout, stderr = self.__client.exec_command(command)
        # stdin.close()
        # for line in stdout.read().splitlines():
        #     print(line)

    # def enable_sftp(self):
    #     """
    #     SFTP를 활성화시킨다.\n
    #     실패시 예외가 발생한다.
    #     """
    #
    #     if not self.__check_client_exists():
    #         raise ClientSshError("Client doesn't exists.")
    #
    #     self.__sftp = paramiko.SFTPClient.from_transport(self.__client.get_transport())

    def __open_self(self, server, username, password, port):
        """
        해당 instance에 SSH Client를 실행한다.\n
        :param server: host name.
        :param username: user name.
        :param password: password.
        :param port: port.
        """

        # SSH Client 생성.
        self.__client = paramiko.SSHClient()

        # SSH Client의 정책 설정.
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        # SSH Client 연결.
        self.__client.connect(
            hostname=server
            , username=username
            , password=password
            , port=port
        )

        self.__is_opened = True

    def __close_self(self):
        """
        해당 instance의 SSH Client를 종료한다.\n
        """
        self.__client.close()

        # if self.__sftp:
        #     self.__sftp.close()

    def __check_client_exists(self):
        """
        해당 instance에 SSH Client가 존재하고 있는지 확인한다.\n
        :return: 확인 결과.
        """
        if self.__client and self.__is_opened:
            return True

        return False

    def __check_command(self, command):
        """
        입력받은 command가 유효한 command인지 검증한다.\n
        :param command: 입력받은 command
        :return: 검증 결과.
        """
        dummy = self

        # command 검증.
        if not isinstance(command, (list, str)):
            raise TypeError("invalid command." + "\n"
                            + "command:" + str(command) + "\n"
                            + "type:" + str(command)
                            )

        # command가 list인 경우의 검증.
        if isinstance(command, list):
            for line in command:
                if type(line) is not str:
                    raise TypeError("invalid command." + "\n"
                                    + "command:" + str(line) + "\n"
                                    + "type:" + str(command)
                                    )

    # @property
    # def server(self):
    #     return self.__server
    #
    # @property
    # def username(self):
    #     return self.__username
    #
    # @property
    # def password(self):
    #     return self.__password
    #
    # @property
    # def port(self):
    #     return self.__port
    #
    # @property
    # def is_opened(self):
    #     return self.__is_opened
