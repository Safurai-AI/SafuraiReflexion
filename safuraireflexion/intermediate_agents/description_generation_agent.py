## Generate Description
from langchain import PromptTemplate
from langchain.llms import OpenAI


class DescriptionGenerationAgent:
    def __init__(self, OPENAI_API_KEY) -> None:
        self.llm = OpenAI(model_name="gpt-3.5-turbo",openai_api_key=OPENAI_API_KEY,temperature=0.1)
        template = """
        First select the method signature from the given code and keep it.
        
        Next, describe the method objective, the inputed parameterers as bullets (try to guess real inputs examples), the flow of steps that describe the code as numerated list, the outputs as bullets (try to guess real outputs examples) and any additional aspect as bullets.


        Given code: {prompt}

        Programming Language:

        Method Signature:

        Description:
            - Objective:
            - Inputs:
            - Flow:
            - Outputs:
            - Additional aspects:

        """

        self.prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template=template
        )

    def create_function_with_comments(self,description, method_signature, programming_language):
        modified_description= "\n".join("\t" + line for line in description.split("\n"))
        result = method_signature + "\n" + '\t"""' + "\n"+ modified_description + "\n" + '\t"""'
        return result

    def generate(self, prompt):
        return self._post_process(self._generate(prompt))

    def _generate(self, prompt):

        result = self.llm(
        self.prompt_template.format(
            prompt=prompt
        ))
        return result
    
    def _post_process(self, result:str):
        result = result.lower()

        split_descripition = result.split("description:")
        rest1 = split_descripition[0]
        
        description = split_descripition[1].strip().lower()

        split_method_signature = rest1.split("method signature:")
        rest2 = split_method_signature[0]
        method_signature = split_method_signature[1].strip().lower().strip(":") + ":"
        
        
        programming_language = rest2.split("programming language:")[1].lower().strip()

        return {
            'description':description,
            'method_signature':method_signature,
            'programming_language':programming_language
            }