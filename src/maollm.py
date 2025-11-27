from openai import OpenAI


class MaoLLM:
    def __init__(self):
        self.llm_client = None
        self.default_llm_model_name = ""

    def update_endpoint(self, base_url, api_key):
        self.llm_client = OpenAI(
            base_url=base_url,
            api_key=api_key,  # ModelScope Token
        )

    def update_llm_model(self, llm_model_name):
        self.default_llm_model_name = llm_model_name

    def parse_inference_stream(self, response):
        thinking_content = ""
        content = ""
        function_call = ""
        finish_reason = ""
        for chunk in response:
            if len(chunk.choices) > 1:
                print(f"WARN: length of chunk.choices is larger than 1: {len(chunk.choices)}")

            if chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content
                print(".", end="", flush=True)

            if chunk.choices[0].delta.function_call:
                function_call += chunk.choices[0].delta.function_call
                print("-", end="", flush=True)

            thinking_chunk = chunk.choices[0].delta.model_extra.get("reasoning_content", None)
            if thinking_chunk:
                thinking_content += thinking_chunk
                print("*", end="", flush=True)

            finish_reason = chunk.choices[0].finish_reason

        print()
        return (thinking_content if thinking_content != "" else None,
                content,
                function_call if function_call != "" else None,
                finish_reason)

    def inference_simple(self, simple_message, model_name=None, stream=True, enable_thinking=False):
        message = self.init_message()
        message.append(self.get_user_message(simple_message))
        return self.inference(message, model_name, stream, enable_thinking)

    def inference(self, context_messages, model_name=None, stream=True, enable_thinking=False):
        """
        返回 response
        """
        if self.llm_client is None:
            return None

        if model_name is None:
            model_name = self.default_llm_model_name

        response = self.llm_client.chat.completions.create(
            model=model_name,
            messages=context_messages,
            stream=stream,
            extra_body={
                "enable_thinking": enable_thinking
            }
        )
        return response

    def init_message(self, system_message_text=None):
        return [{
            'role': 'system',
            'content': system_message_text
        }] if system_message_text else []

    def get_user_message(self, message_text):
        return {
            'role': 'user',
            'content': message_text
        }

    def get_assistant_message(self, message_text):
        return {
            'role': 'assistant',
            'content': message_text
        }

    # TODO: Tool request
    # TODO: Tool response
