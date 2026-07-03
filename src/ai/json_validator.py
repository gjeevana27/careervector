class JSONValidator:

    @staticmethod
    def validate(data: dict, required_keys: list):

        if not isinstance(data, dict):
            raise Exception("AI response is not a dictionary.")

        missing = []

        for key in required_keys:

            if key not in data:
                missing.append(key)

        if missing:

            raise Exception(
                f"Missing required keys: {', '.join(missing)}"
            )

        return True