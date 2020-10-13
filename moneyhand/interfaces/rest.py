from moneyhand.core.service import Service


class RESTInterface:
    service: Service

    def __init__(self, service: Service):
        self.service = service

    async def run(self):
        print(self.service)
