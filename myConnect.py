import urequests as requests


class myConnect:
    def __init__(self):
        self.keys = self.readEnv("config.txt")


    def __str__(self) -> str:
        return '<myConnectObject>'


    # custom implementation of reading config files
    def readEnv(self, file):
        env_file = open(file, "r")
        env_dict = {}

        for kv_pair in env_file:
            line = kv_pair.strip().split("=", 1)
            # no dangling spaces
            line = [x.strip() for x in line]
            env_dict[line[0]] = line[1]

        env_file.close()

        return env_dict


    def sendNtfy(self, title, message):
        head = {'Authorization': 'Basic {}'.format(self.keys["SERVER_AUTH"]), 'Title': str(title)}
        response = requests.post(self.keys["SERVER_URL"], headers=head, data=message)
        status = response.status_code
        response.close()
        return status


    def pushToInflux(self, bucket, linedata):
        url=self.keys["INFLUX_URL"] + "&bucket={}".format(bucket)
        head = {'Authorization': 'Token {}'.format(self.keys["INFLUX_AUTH"])}
        response = requests.post(url, headers=head, data=linedata)
        status = response.status_code
        response.close()
        return status
