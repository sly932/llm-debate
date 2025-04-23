"""
主程序入口

此模块实现了LLM辩论的主要流程。
"""

import argparse
import uuid
from typing import Dict, Optional, Any

from src.debate_engine import DebateEngine
from utils.data_utils import DataManager
from utils.logger import setup_logger

# 设置日志记录器
logger = setup_logger(log_file="logs/llm_debate.log")

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="LLM辩论系统")
    parser.add_argument("--query", type=str, help="用户查询")
    parser.add_argument("--model_1", type=str, default="deepseek-v3-friday", help="正房使用的LLM模型")
    parser.add_argument("--model_2", type=str, default="deepseek-v3-friday", help="反方使用的LLM模型")
    parser.add_argument("--analysis_model", type=str, default="deepseek-v3-friday", help="拆解论点使用的LLM模型")
    parser.add_argument("--cycles", type=int, default=3, help="辩论回合数")
    parser.add_argument("--save", action="store_true",default=True, help="是否保存辩论结果")
    parser.add_argument("--debug", action="store_true", help="是否启用调试模式")

    return parser.parse_args()

def run_debate(query: str, model_name_1: str, model_name_2:str, analysis_model_name, cycle_times: int) -> Dict[str, Any]:
    """
    运行辩论流程

    Args:
        query: 用户查询
        model_name: 使用的LLM模型名称
        cycle_times: 辩论回合数

    Returns:
        Dict[str, Any]: 辩论结果
    """
    logger.info(f"开始辩论，查询：{query}，模型1：{model_name_1}，模型2：{model_name_2}，回合数：{cycle_times}")

    # 创建辩论引擎
    debate_engine = DebateEngine(model_name_1, model_name_2, analysis_model_name, cycle_times,affirmative_role="role1",negative_role="role2")

    # 运行辩论
    debate_result = debate_engine.run_debate(query)

    logger.info(f"辩论完成，主题：{debate_result['topic']}")

    return debate_result

def save_debate_result(debate_result: Dict[str, Any], save: bool = True) -> Optional[str]:
    """
    保存辩论结果

    Args:
        debate_result: 辩论结果
        save: 是否保存

    Returns:
        Optional[str]: 保存的文件路径，如果不保存则返回None
    """
    if not save:
        return None

    # 创建数据管理器
    data_manager = DataManager()

    # 生成辩论ID
    debate_id = str(uuid.uuid4())

    # 保存辩论结果
    file_path = data_manager.save_debate(debate_id, debate_result)

    logger.info(f"辩论结果已保存到：{file_path}")

    return file_path

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()

    # 设置日志级别
    if args.debug:
        logger.setLevel("DEBUG")

    # 获取用户查询
    query = args.query
    if not query:
        # query = input("请输入您的问题：")
        query = "我在做Agent应用开发，应该看英文文档还是翻译成中文文档再阅读。"

    # 运行辩论
    debate_result = run_debate(query, args.model_1, args.model_2, args.analysis_model, args.cycles)

    # 保存辩论结果
    if args.save:
        save_debate_result(debate_result)

if __name__ == "__main__":
    main()

