import mistune
from mistune.plugins import _plugins

from maollm import MaoLLM

class MaoAgent():
    def __init__(self):
        self.llm_module = MaoLLM()

    def main(self):
        self.llm_module.update_endpoint(
            "https://open.bigmodel.cn/api/paas/v4",
            "this-is-api-key")
        self.llm_module.update_llm_model("glm-4.5-flash")
        response = self.llm_module.inference([{"role":"user","content":"输出markdown格式的内容，以下是用户请求：青岛"}])
        result = self.llm_module.parse_inference_stream(response)

        with open("qingdao.md", mode="w", encoding="utf-8") as f:
            f.write(result[1])

        with open("qingdao.html", mode="w", encoding="utf-8") as f:
            md = mistune.create_markdown(
                escape=True,  # 转义特殊字符（防止XSS）
                hard_wrap=True,  # 换行符转为 <br>
                plugins=[k for k in _plugins]
            )
            html = md(result[1])
            f.write(html)

        print(result)

if __name__ == "__main__":
    agent = MaoAgent()
    agent.main()
