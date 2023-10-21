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
SYSMSG_KIDS = os.environ.get("SYSMSG_KIDS")
SYSMSG_PARENTS = os.environ.get("SYSMSG_PARENTS")

#chatbot class
class ChatbotWithHistory:
    def __init__(self, is_for_kids: bool):
        if is_for_kids:
            self.template = SYSMSG_KIDS
        else:
            self.template = SYSMSG_PARENTS

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
            GenParams.LENGTH_PENALTY: {'decay_factor': 2.5, 'start_index': 150}
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
        if len(inp['history']) > 0:
            prev_prompts = retreive_hist(inp)
            #running cosine similarity on the entire chat history to retreive the most relevant messages
            n_prompts_answers = cossimhist(last_prompt_emb, vec_dict=prev_prompts)

            prompt_formatted_str = self.prompt.format(chat_history=n_prompts_answers, human_input=last_prompt_str)
            
            response = self.chain(prompt_formatted_str, last_prompt_str)
        else:
            prompt_formatted_str = self.template.format(chat_history=last_prompt_str, human_input=last_prompt_str)
            response = self.chain(last_prompt_str)

        return response