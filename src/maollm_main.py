from maollm import MaoLLM


def main():
    llm = MaoLLM()
    llm.update_endpoint("http://127.0.0.1:8080/v1", "mao")
    llm.update_llm_model("Qwen3-0.6B-gguf-Q8_0.gguf")

    messages = llm.init_message('You are a helpful assistant.')
    messages.append(llm.get_user_message("青岛"))

    response = llm.inference(messages)
    _, content, _, _ = llm.parse_inference_stream(response)
    print(content)

    response = llm.inference_simple("海口")
    _, content, _, _ = llm.parse_inference_stream(response)
    print(content)


if __name__ == "__main__":
    main()
