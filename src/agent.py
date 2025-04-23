"""
辩论代理模块

此模块实现了辩论代理类，用于处理辩论过程中的代理行为。
"""

from typing import Dict, List, Optional
from utils.llm_utils import LLMClient


class DebateAgent:
    """辩论代理类，用于处理辩论过程中的代理行为"""

    def __init__(
        self,
        model_name: str,
        stance: str,
        role: Optional[str] = None,
        role_background: Optional[str] = None,
        role_knowledge: Optional[str] = None,
        role_style: Optional[str] = None,
    ):
        """
        初始化辩论代理

        Args:
            model_name: 使用的LLM模型名称
            stance: 代理的立场（正方或反方）
            role: 代理的角色名称
            role_background: 角色背景
            role_knowledge: 角色知识领域
            role_style: 角色辩论风格
        """
        self.model_name = model_name
        self.stance = stance
        self.role = role or f"{stance}方辩手"
        self.role_background = role_background or ""
        self.role_knowledge = role_knowledge or ""
        self.role_style = role_style or ""
        self.history = []

    def initialize(self, topic: str, argument: str = "", first_talk: bool = False) -> str:
        """
        初始化辩论，生成开场白

        Args:
            topic: 辩论主题
            argument: 预设的论点
            first_talk: 是否首次说话

        Returns:
            str: 代理的开场白
        """
        system_prompt = self._build_system_prompt(topic, argument)
        self.history.append({"role": "system", "content": system_prompt})
        if first_talk:
            user_prompt = f"针对问题<{topic}>，从<{argument}>的角度出发给我回答。"
            self.history.append({"role": "user", "content": user_prompt})
            initial_argument = LLMClient.get_client().generate(msgs=self.history)
            self.history.append({"role": "assistant", "content": initial_argument})
            return initial_argument
        return ""

    def respond(self, model_name, opponent_argument: str, round_number: int) -> str:
        """
        对对方的论点进行回应

        Args:
            model_name: 使用的LLM模型名称
            opponent_argument: 对方的论点
            round_number: 当前回合数

        Returns:
            str: 代理的回应
        """
        self.history.append({"role": "user", "content": opponent_argument})
        response = LLMClient.get_client(model_name).generate(msgs=self.history)
        self.history.append({"role": "assistant", "content": response})
        return response

    def conclude(self, topic: str) -> str:
        """
        生成结论陈述

        Args:
            topic: 辩论主题

        Returns:
            str: 代理的结论陈述
        """
        # 这里应该调用LLM API，使用结论提示词生成结论
        # 实际实现时需要替换为真实的LLM调用
        conclusion = f"这是{self.role}的结论陈述，立场是{self.stance}，主题是{topic}"
        self.history.append({"role": "assistant", "content": conclusion})
        return conclusion

    def get_history(self) -> List[Dict[str, str]]:
        """
        获取代理的对话历史

        Returns:
            List[Dict[str, str]]: 对话历史列表
        """
        return self.history

    def _build_system_prompt(self, topic, argument):
        from prompts.agent_debate_prompt import AGENT_DEBATE_SYSTEM_PROMPT
        prompt = AGENT_DEBATE_SYSTEM_PROMPT.replace(f"{topic}", topic)
        prompt = prompt.replace(f"{argument}", argument)
        return prompt

