# Python 内置的异步编程库，让 MCP 可以非阻塞地执行任务（比如聊天、查询）。
import asyncio
# 用于管理 MCP 客户端会话（但目前我们先不连接 MCP 服务器）。
from mcp import ClientSession
# 自动管理资源，确保程序退出时正确关闭 MCP 连接。
from contextlib import AsyncExitStack


"""
这段代码能够初始化 MCP 客户端（但不连接服务器），并提供一个 交互式 CLI，可以输入查询（但只返回模拟回复），
通过输入 quit 退出程序。
需要注意的是，此时客户端没有关联任何大模型，因此只会重复用户的输入。

运行这个极简的MCP客户端：
uv run simple-mcp-client.py
"""

class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.session = None # 暂时不连接 MCP 服务器，后续可以修改来真正连接。
        self.exit_stack = AsyncExitStack() # 管理 MCP 客户端的资源，确保程序退出时可以正确释放资源。

    async def connect_to_mock_server(self):
        """模拟 MCP 服务器的连接（暂不连接真实服务器）"""
        print("✅ MCP 客户端已初始化，但未连接到服务器")

    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("\nMCP 客户端已启动！输入 'quit' 退出")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break
                print(f"\n🤖 [Mock Response] 你说的是：{query}")
            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()

async def main():
    client = MCPClient() # 创建 MCP 客户端
    try:
        await client.connect_to_mock_server() # 连接（模拟）服务器
        await client.chat_loop() # 启动交互式聊天
    finally:
        await client.cleanup() # 确保退出时清理资源

if __name__ == "__main__":
    asyncio.run(main())