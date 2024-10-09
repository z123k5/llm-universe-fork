"""Chain that makes API calls and summarizes the responses to answer a question."""
from __future__ import annotations

from qa_chain.MyAPIChain.prompt import API_URL_PROMPT

from typing import Any, Dict, List, Optional

from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
# from langchain.chains.api.prompt import API_RESPONSE_PROMPT, API_URL_PROMPT
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain.pydantic_v1 import Field, root_validator
from langchain.schema import BasePromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from langchain.utilities.requests import TextRequestsWrapper


class MyAPIChain(Chain):
    """Chain that makes API calls and summarizes the responses to answer a question."""

    api_request_chain: LLMChain
    requests_wrapper: TextRequestsWrapper = Field(exclude=True)
    api_docs: str
    question_key: str = "question"  #: :meta private:
    output_key: str = "output"  #: :meta private:
    userId: int = 0         #: :meta private:

    @property
    def input_keys(self) -> List[str]:
        """Expect input key.

        :meta private:
        """
        return [self.question_key]

    @property
    def output_keys(self) -> List[str]:
        """Expect output key.

        :meta private:
        """
        return [self.output_key]
    
    @property
    def user_id(self) -> int:
        """Expect user id.

        :meta private:
        """
        return self.userId

    @root_validator(pre=True)
    def validate_api_request_prompt(cls, values: Dict) -> Dict:
        """Check that api request prompt expects the right variables."""
        input_vars = values["api_request_chain"].prompt.input_variables
        expected_vars = {"question", "api_docs", "context"}
        if set(input_vars) != expected_vars:
            raise ValueError(
                f"Input variables should be {expected_vars}, got {input_vars}"
            )
        return values

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()

        context = ["用户的userId:"+str(self.userId)+"(特别注意，记住)"]
        loopTimes = 0
        question = inputs[self.question_key]
        api_response = ""
        while loopTimes < 5:
            loopTimes += 1
            api_url = self.api_request_chain.predict(
                question=question,
                context=context,
                api_docs=self.api_docs,
                callbacks=_run_manager.get_child(),
            )
            start_index = api_url.find("http://")
            lf_index = api_url.find("\n")

            extracted_url = ""
            extracted_second = ""
            if lf_index != -1:
                extracted_url = api_url[start_index:lf_index]
                extracted_second = api_url[lf_index:]
            else:
                extracted_url = api_url[start_index:]
                if not extracted_url.find("http://"):
                    extracted_second = api_url
            
            # 判断是否有效的url
            if extracted_url.find("http://") != -1:
                _run_manager.on_text(extracted_url + '\n' + extracted_second, color="green",
                                    end="\n", verbose=self.verbose)
                try:
                    api_response = self.requests_wrapper.get(extracted_url)
                except Exception as e:
                    api_response = str(e)
                _run_manager.on_text(
                    api_response, color="yellow", end="\n", verbose=self.verbose
                )
                context.append(extracted_second + api_response)
                if api_url[-10:].rfind("done") != -1:
                    break
            else:
                break

        return {self.output_key: context}

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()

        context = ["用户的userId:"+str(self.userId)+"(特别注意，记住)"]
        loopTimes = 0
        question = inputs[self.question_key]
        api_response = ""
        while loopTimes < 5:
            loopTimes += 1
            api_url = await self.api_request_chain.apredict(
                question=question,
                context=context,
                api_docs=self.api_docs,
                callbacks=_run_manager.get_child(),
            )
            start_index = api_url.find("http://")
            lf_index = api_url.find("\n")

            extracted_url = ""
            extracted_second = ""
            if lf_index != -1:
                extracted_url = api_url[start_index:lf_index]
                extracted_second = api_url[lf_index:]
            else:
                extracted_url = api_url[start_index:]

            # 判断是否有效的url
            if extracted_url.find("http://") != -1:
                await _run_manager.on_text(extracted_url + '\n' + extracted_second, color="green",
                                     end="\n", verbose=self.verbose)
                try:
                    api_response = await self.requests_wrapper.aget(extracted_url)
                except Exception as e:
                    api_response = str(e)
                await _run_manager.on_text(
                    api_response, color="yellow", end="\n", verbose=self.verbose
                )
                context.append(api_response)
            else:
                break

        return {self.output_key: str(api_response)}

    @classmethod
    def from_llm_and_api_docs(
        cls,
        llm: BaseLanguageModel,
        api_docs: str,
        headers: Optional[dict] = None,
        api_url_prompt: BasePromptTemplate = API_URL_PROMPT,
        # api_response_prompt: BasePromptTemplate = API_RESPONSE_PROMPT,
        userId: int = 0,
        **kwargs: Any,
    ) -> MyAPIChain:
        """Load chain from just an LLM and the api docs."""
        get_request_chain = LLMChain(llm=llm, prompt=api_url_prompt)
        requests_wrapper = TextRequestsWrapper(headers=headers)
        # get_answer_chain = LLMChain(llm=llm, prompt=api_response_prompt)
        return cls(
            api_request_chain=get_request_chain,
            # api_answer_chain=get_answer_chain,
            requests_wrapper=requests_wrapper,
            api_docs=api_docs,
            userId=userId,
            **kwargs,
        )

    @property
    def _chain_type(self) -> str:
        return "my_api_chain"
