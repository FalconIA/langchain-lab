# Copyright 2023 Lei Zhang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List

from langchain import LLMChain, PromptTemplate
from langchain.chat_models.base import BaseChatModel
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage

from src.langchain_lab.core.llm import TrackerCallbackHandler

default_system_message = """You are a nice chatbot having a conversation with a human.
"""

human_message_template = """{question}
ASSISTANT:"""

def chat_once(query: str, llm: BaseChatModel, prompt: PromptTemplate, callback: TrackerCallbackHandler = None):
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        callbacks=[callback],
    )
    return chain.run(query)


def chat(
    query: str,
    llm: BaseChatModel,
    system_message: str = None,
    callback: TrackerCallbackHandler = None,
    chat_history: List = None,
):
    if system_message is None or len(system_message) == 0:
        system_message = default_system_message

    if chat_history is not None:
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template)

        # Append chat history to system message if chat history is not empty
        if '{chat_history}' not in system_message:
            system_message = system_message + "\n{chat_history}"

        if len(chat_history) > 0:
            # chat_history_string = "\n".join([message + '\n' if i % 2 == 1 else message for i, message in enumerate(chat_history)])
            chat_history_string = "\n".join(chat_history)
        else:
            chat_history_string = ""
        system_message_prompt = SystemMessage(
            content=system_message.format(chat_history=chat_history_string))
    else:
        template = "{question}"
        system_message_prompt = SystemMessage(content=system_message)
        human_message_prompt = HumanMessagePromptTemplate.from_template(template)

    inputs = {"question": query}
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(
        llm=llm,
        prompt=chat_prompt,
        callbacks=[callback],
    )
    response = chain.run(inputs)
    return response
