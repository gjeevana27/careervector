from groq import Groq

from src.core.config import settings


class AIClient:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.MODEL_NAME

    def generate(self, system_prompt, user_prompt):

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],

            temperature=0,

            response_format={
                "type": "json_object"
            }

        )

        content = response.choices[0].message.content

        print("\n")
        print("=" * 100)
        print("RAW GROQ RESPONSE")
        print("=" * 100)
        print(content)
        print("=" * 100)
        print("\n")

        return content