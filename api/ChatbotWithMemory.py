from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
import os
from os.path import dirname, join 
from dotenv import load_dotenv
from .vecdb import cossimhist, retreive_hist 

#.env adjustments
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
API_TOKEN = os.environ.get("APIKEY")
PROJECT_ID = os.environ.get("PROJECT_ID")
SYSMSG_CHAT = os.environ.get("SYSMSG")

#chatbot class
class ChatbotWithHistory:
    def __init__(self):
        # self.prompt = 'Act as a helpful virtual psychology assistant that provides emotional support and friendly advice to children in a critical situation, situation of stress and trouble. You should provide the user with correct, guiding information. Upon receiving a prompt reply to the user immediately, without augmenting their prompt. DO NOT model a dialogue -- give them time to in turn reply to you. Assume that the prompt the user inputs is complete and there is no need for you to add anything to it. ===PROMPT START=== {userinput} ===PROMPT END===\n'
        # self.template = 'Act as a helpful virtual psychology assistant that provides emotional support and friendly advice to children in a critical situation, situation of stress and trouble. You should provide the user with correct, guiding information. Upon receiving a prompt reply to the user immediately, without augmenting their prompt. DO NOT model a dialogue -- give them time to in turn reply to you. Assume that the prompt the user inputs is complete and there is no need for you to add anything to it. ===PROMPT START=== {userinput} ===PROMPT END==='
        
        self.template = SYSMSG_CHAT

        self.prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"],
            template=self.template
        )

        GenParams().get_example_values()

        #model hyperparameters 
        self.generate_params = {
            GenParams.MIN_NEW_TOKENS: 10,
            GenParams.MAX_NEW_TOKENS: 250,
            GenParams.TEMPERATURE: 0.0,
            GenParams.REPETITION_PENALTY: 1,
        }

        #initializing the model 
        self.model = Model(
            model_id=ModelTypes.LLAMA_2_70B_CHAT,
            params=self.generate_params,
            credentials={
                "apikey": API_TOKEN,  
                "url": "https://eu-de.ml.cloud.ibm.com"
            },
            project_id=PROJECT_ID
        )

        self.memory = ConversationBufferMemory(
            memory_key='chat_history',
            input_key='human_input'
        )

        self.chain = LLMChain(llm=self.model.to_langchain(), prompt=self.prompt, verbose=False, memory=self.memory)

    #a method to get the model's response to some prompt + history 
    def get_response(self, inp: dict):
        last_prompt_str = inp['new_prompt']['prompt'] #str of the last prompt
        last_prompt_emb = inp['new_prompt']['vectorized_prompt'] #embedding of the last prompt
        prompt_formatted_str = self.template.format(chat_history=None, human_input=last_prompt_str)


        #handling an empty database 
        if len(inp['history']) != 0:
            prev_prompts = retreive_hist(inp)
            #running cosine similarity on the entire chat history to retreive the most relevant messages
            n_prompts_answers = cossimhist(last_prompt_emb, vec_dict=prev_prompts)

            prompt_formatted_str = self.template.format(chat_history=n_prompts_answers, human_input=last_prompt_str)
            
            response = self.chain(prompt_formatted_str, last_prompt_str)
        else:
            prompt_formatted_str = self.template.format(chat_history=last_prompt_str, human_input=last_prompt_str)
            response = self.chain(last_prompt_str)

        return response

#executing the file 
# if __name__ == "__main__":
#     chatbot = ChatbotWithHistory()
#     inp = {'new_prompt': {
#         'prompt': 'hey, let`s talk',
#         'vectorized_prompt': None
#     },
#     'history': []
#     }

#     response = chatbot.get_response(inp)
#     print(response['text'])