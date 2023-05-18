from langchain import PromptTemplate
from langchain.llms import OpenAI

class FunctionMocksAgent:
    def __init__(self,OPENAI_API_KEY) -> None:
        self.llm = OpenAI(model_name="gpt-3.5-turbo",openai_api_key=OPENAI_API_KEY,temperature=0.1)
        template = """
        You are a code assitant the knows how to use mocked unit tests. Any extenal library in the given code must me mocked to avoid importing it using the framwrok unittest. Rewrite the given code only replacing an external libray for mock. Make sure it wont give any error.
        Instead of import packages replace them you can create mock methods/classes that act as them.
        Never write text that is not code.

        Example: requests.get = Mock()

        Given code: {prompt}

        Suggested mocked methods and classes:
        """

        self.prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template=template
        )
    def generate(self, prompt):

        result = self.llm(
        self.prompt_template.format(
            prompt=prompt
        ))
        return result