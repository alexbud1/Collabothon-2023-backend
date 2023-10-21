from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from langchain import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import ZeroShotAgent, AgentExecutor, Tool, load_tools
import os
from os.path import dirname, join 
from dotenv import load_dotenv

# .env adjustments
dotenv_path = join(dirname(dirname(__file__)), ".env")
load_dotenv(dotenv_path)
API_TOKEN = os.environ.get("APIKEY")
PROJECT_ID = os.environ.get("PROJECT_ID")

#chatbot class
class ChatbotWithHistory:
    def __init__(self):
        # self.prompt = 'Act as a helpful virtual psychology assistant that provides emotional support and friendly advice to children in a critical situation, situation of stress and trouble. You should provide the user with correct, guiding information. Upon receiving a prompt reply to the user immediately, without augmenting their prompt. DO NOT model a dialogue -- give them time to in turn reply to you. Assume that the prompt the user inputs is complete and there is no need for you to add anything to it. ===PROMPT START=== {userinput} ===PROMPT END===\n'
        # self.template = 'Act as a helpful virtual psychology assistant that provides emotional support and friendly advice to children in a critical situation, situation of stress and trouble. You should provide the user with correct, guiding information. Upon receiving a prompt reply to the user immediately, without augmenting their prompt. DO NOT model a dialogue -- give them time to in turn reply to you. Assume that the prompt the user inputs is complete and there is no need for you to add anything to it. ===PROMPT START=== {userinput} ===PROMPT END==='
        
        self.template = """Act as a helpful virtual psychology assistant that provides emotional support and friendly advice to children in a critical situation, situation of stress and trouble. You should provide the user with correct, guiding information. Upon receiving a prompt reply to the user immediately, without augmenting their prompt. DO NOT model a dialogue -- give them time to in turn reply to you. Assume that the prompt the user inputs is complete and there is no need for you to add anything to it.
        {chat_history}
        Human: {human_input}
        Chatbot:"""

        self.prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"], template=self.template
        )

        GenParams().get_example_values()

        #model hyperparameters 
        self.generate_params = {
            GenParams.MIN_NEW_TOKENS: 10,
            GenParams.MAX_NEW_TOKENS: 250,
            GenParams.TEMPERATURE: 0,
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
        #initializing langchain 
        # self.llm_chain = LLMChain(llm=self.model.to_langchain(), prompt=PromptTemplate.from_template(self.prompt))
        self.memory = ConversationBufferMemory(memory_key='chat_history')
        self.llm_chain = LLMChain(llm=self.model.to_langchain(), prompt=self.prompt, verbose=True, memory=self.memory)

        #giving the model memory
        # self.conversation = ConversationChain(
        #     llm=self.llm_chain, 
        #     verbose=True,
        #     memory=ConversationBufferMemory())
        # self.agent = ZeroShotAgent(llm_chain=self.llm_chain, verbose=True)
        # self.agent_chain = AgentExecutor.from_agent_and_tools(agent=self.agent, verbose=True, memory=self.memory)

    #a function to get the model's response to some prompt 
    def get_response(self, user_input):
        # self.conversation_history += "Użytkownik: " + user_input + '\n'
        # generated_response = self.model.generate(prompt=self.conversation_history)
        # bot_response = generated_response['results'][0]['generated_text']
        # self.conversation_history += "Chatbot: " + bot_response + '\n'

        prompt = user_input
        bot_response = self.llm_chain(prompt)
        return bot_response


#executing the file 
if __name__ == "__main__":
    chatbot = ChatbotWithHistory()

    #a continuous 'chat' loop
    while True:
        user_message = input("Ty: ")
        if user_message.lower() in ['exit', 'quit']:
            break
        response = chatbot.get_response(user_message)
        print("Chatbot:", response)
    # response = chatbot.get_response('hey, my name is el. let`s talk')
    # print(response)