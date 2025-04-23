"""
辩论引擎模块

此模块实现了辩论引擎类，用于协调整个辩论流程。
"""
import json
from typing import Dict, Tuple, Optional, Any

from src.agent import DebateAgent

from utils.llm_utils import LLMClient


class DebateEngine:
    """辩论引擎类，用于协调整个辩论流程"""

    def __init__(
        self,
        model_name_1: str,
        model_name_2: str,
        analysis_model_name: str,
        cycle_times: int = 3,
        affirmative_role: Optional[str] = None,
        negative_role: Optional[str] = None,
    ):
        """
        初始化辩论引擎

        Args:
            model_name_1: 正方模型名称
            model_name_2: 反方模型名称
            analysis_model_name: 分析模型名称
            cycle_times: 辩论回合数
            affirmative_role: 正方角色名称
            negative_role: 反方角色名称
        """
        self.model_name_1 = model_name_1
        self.model_name_2 = model_name_2
        self.analysis_model_name = analysis_model_name
        self.cycle_times = cycle_times
        self.affirmative_agent = DebateAgent(model_name_1, "正方", affirmative_role)
        self.negative_agent = DebateAgent(model_name_2, "反方", negative_role)
        self.debate_history = []

    def analyze_query(self, query: str) -> Tuple[str, str, str]:
        """
        分析用户查询，提取辩论主题和正反方论点

        Args:
            query: 用户查询

        Returns:
            Tuple[str, str, str]: 主题、正方论点、反方论点
        """
        # 这里应该调用LLM API，使用查询分析提示词提取主题和论点
        # 实际实现时需要替换为真实的LLM调用
        prompt = """
        你是一个辩论助手，你的任务是分析用户查询，提取主题和两个论点。
        # 用户查询
        {query}
        # 注意
        不需要进行论点解释，只需要提取主题和论点即可。例如，提问应该A还是B，论点为‘应该A’和‘应该B’，不要进行解释。
        # 输出格式
        - json格式返回,直接返回json字符串，不要在json外加任何字符（例如```json ```等）
        - {
        "topic":"xxx",
        "argument_1":"xxx",
        "argument_2":"xxx"
        }
        """
        prompt = prompt.replace("{query}", query)
        msgs = [{"role": "user", "content": prompt}]
        response = LLMClient.get_client(self.analysis_model_name).generate(msgs=msgs)
        try:
            response = json.loads(response)
            topic = response["topic"]
            affirmative_argument = response["argument_1"]
            negative_argument = response["argument_2"]
        except Exception as e:
           raise ValueError(f"分析查询失败：{e}")

        return topic, affirmative_argument, negative_argument

    def run_debate(self, query: str) -> Dict[str, Any]:
        """
        运行辩论流程

        Args:
            query: 用户查询

        Returns:
            Dict[str, Any]: 辩论结果，包含辩论历史和总结
        """
        # 分析查询，提取主题和论点
        topic, affirmative_argument, negative_argument = self.analyze_query(query)

        # 正方先发表观点
        affirmative_opening = self.affirmative_agent.initialize(topic, affirmative_argument, True)
        self.negative_agent.initialize(topic, negative_argument)

        # 记录正方开场白
        self.debate_history.append({
            "role":self.affirmative_agent.role,
            "msg":affirmative_opening
            }
        )

        # 进行多轮辩论
        for round_num in range(1, self.cycle_times + 1):
            print(f"{self.affirmative_agent.role}:<{affirmative_argument}> ({self.model_name_1})")
            print(f"{self.debate_history[-1]['msg']}")

            # 反方回应正方
            negative_response = self.negative_agent.respond(
                self.model_name_2,
                self.debate_history[-1]['msg'],
                round_num
            )
            self.debate_history.append({
                "role":self.negative_agent.role,
                "msg":negative_response})

            print(f"{self.negative_agent.role}:<{negative_argument}> ({self.model_name_2})")
            print(f"{self.debate_history[-1]['msg']}")

            # 正方回应反方
            affirmative_response = self.affirmative_agent.respond(
                self.model_name_1,
                negative_response,
                round_num
            )
            self.debate_history.append({
                "role":self.affirmative_agent.role,
                "msg":affirmative_response})

        return {
            "topic": topic,
            "affirmative_argument": affirmative_argument,
            "negative_argument": negative_argument,
            "debate_history": self.debate_history
        }

