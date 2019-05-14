import requests

class Sender():
    def __init__(self):
        # self.host = '192.168.0.100'
        self.host = '10.42.0.235'
        self.port = '8000'
        self.base_url = 'http://' + self.host + ':'+ self.port + '/'
        if(not self.connection_ok()):
            raise Exception('Connection failed')
    
    def send_action(self, action):
        self.run_action(action)

    def run_action(self, action):
        url = self.base_url + 'run/?action=' + str(action)
        print(url)
        self.__request__(url)
    
    def __request__(self, url, times=10):
        for _ in range(times):
            try:
                requests.get(url)
                return 0
            except Exception as e:
                print('connection error, try again')
                # print(str(e))
        print('abort')
        return -1
        # pass
    
    def connection_ok(self):
        """Check whetcher connection is ok

        Post a request to server, if connection ok, server will return http response 'ok' 

        Args:
            none

        Returns:
            if connection ok, return True
            if connection not ok, return False
        
        Raises:
            none
        """
        cmd = 'connection_test' + "/"
        url = self.base_url + cmd
        print('url: %s'% url)
        # if server find there is 'connection_test' in request url, server will response 'Ok'
        try:
            r=requests.get(url)
            if r.text == 'OK':
                return True
        except:
            return False
