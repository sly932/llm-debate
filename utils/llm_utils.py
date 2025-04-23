"""
LLM工具模块

此模块提供了与LLM交互的工具函数。
"""

from typing import Dict, List, Optional, Any
from openai import OpenAI


class LLMClient:
    """LLM客户端类，用于处理与LLM的交互（单例模式）"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式

        Returns:
            LLMClient: 单例实例
        """
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_name: str = None):
        """
        初始化LLM客户端
        Args:
            model_name: 使用的LLM模型名称
            api_key: API密钥
        """
        # 确保初始化只执行一次
        if self._initialized:
            return

        self.model_name = model_name
        self.client = OpenAI(base_url="https://aigc.sankuai.com/v1/openai/native/",
               api_key="1714125195532980318")
        # 实际实现时需要初始化相应的LLM客户端
        self._initialized = True

    @classmethod
    def get_client(cls, model_name: str = None):
        """
        获取LLMClient实例

        Args:
            model_name: 使用的LLM模型名称
            api_key: API密钥

        Returns:
            LLMClient: 单例实例
        """
        if cls._instance is None:
            return cls(model_name)

        # 如果提供了新的参数，更新实例
        if model_name is not None:
            cls._instance.model_name = model_name

        return cls._instance

    def generate(
        self,
        msgs: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        生成文本

        Args:
            msgs: 消息列表
            temperature: 采样温度
            max_tokens: 最大生成token数
        Returns:
            str: 生成的文本
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=msgs,
            temperature=temperature,
            max_tokens=max_tokens)
        return response.choices[0].message.content

    def extract_arguments(self, query: str) -> Dict[str, str]:
        """
        从用户查询中提取辩论主题和正反方论点

        Args:
            query: 用户查询

        Returns:
            Dict[str, str]: 包含主题和论点的字典
        """
        # 实际实现时需要调用相应的LLM API
        return {
            "topic": query,
            "affirmative_argument": f"正方论点：支持{query}",
            "negative_argument": f"反方论点：反对{query}"
        }

    def summarize_debate(
        self,
        topic: str,
        debate_history: List[Dict[str, Any]]
    ) -> str:
        """
        总结辩论结果

        Args:
            topic: 辩论主题
            debate_history: 辩论历史

        Returns:
            str: 辩论总结
        """
        # 实际实现时需要调用相应的LLM API
        return f"这是关于主题<{topic}>的辩论总结"

