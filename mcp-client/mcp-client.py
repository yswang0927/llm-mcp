# Python 内置的异步编程库，让 MCP 可以非阻塞地执行任务（比如聊天、查询）。
import asyncio
# 自动管理资源，确保程序退出时正确关闭 MCP 连接。
from contextlib import AsyncExitStack
import os
from openai import OpenAI
from dotenv import load_dotenv


"""
这段代码能够初始化 MCP 客户端（但不连接服务器），并提供一个 交互式 CLI，
并使用 OpenAI 连接到大模型，
通过输入 quit 退出程序。

运行这个MCP客户端：
uv run mcp-client.py
"""

# 加载 .env 文件，确保 API Key 受到保护
load_dotenv()

class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.exit_stack = AsyncExitStack()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")  # 读取 OpenAI API Key
        self.base_url = os.getenv("BASE_URL")  # 读取 BASE YRL
        self.model = os.getenv("MODEL")  # 读取 model

        if not self.openai_api_key:
            raise ValueError("❌ 未找到 OpenAI API Key，请在 .env 文件中设置 OPENAI_API_KEY")

        self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)


    async def process_query(self, query: str) -> str:
        """调用 OpenAI API 处理用户查询"""
        messages = [{"role": "system", "content": "你是一个智能助手，帮助用户回答问题。"},
                    {"role": "user", "content": query}]

        try:
            # 调用 OpenAI API
            # 因为 OpenAI API 是同步的，但我们用的是异步代码，
            # 这里用 asyncio.get_event_loop().run_in_executor(...)
            # 将 OpenAI API 变成异步任务，防止程序卡顿。
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=10000,
                    temperature=0.7 #控制 AI 回答的随机性（越高越随机）
                )
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ 调用 OpenAI API 时出错: {str(e)}"


    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("\nMCP 客户端已启动！输入 'quit' 退出")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break

                # 发送用户输入到 OpenAI API
                response = await self.process_query(query)
                print(f"\n🤖 OpenAI: {response}")

            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")


    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()


async def main():
    client = MCPClient()
    try:
        await client.chat_loop() # 启动交互式聊天
    finally:
        await client.cleanup() # 确保退出时清理资源

if __name__ == "__main__":
    asyncio.run(main())