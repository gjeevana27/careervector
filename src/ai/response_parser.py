import json


class ResponseParser:

    @staticmethod
    def parse(response):

        print("\n")
        print("=" * 100)
        print("PARSER RECEIVED")
        print("=" * 100)
        print(response)
        print("=" * 100)
        print("\n")

        return json.loads(response)