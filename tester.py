#!/usr/bin/env python3
"""
perf-test-assistant: Local AI performance test assistant using Ollama.
"""

import argparse
import ollama

MODEL = "qwen2.5:7b"


def generate_locust_script(api_info: str, users: int = 100, duration: str = "60s") -> str:
    """Generate Locust performance test script."""
    prompt = f"""你是一个资深性能测试工程师。请根据以下信息生成Locust性能测试脚本。

接口信息：
{api_info}

并发用户数：{users}
压测时长：{duration}

要求：
1. 使用Python + Locust框架
2. 包含完整的用户行为模拟（任务组、权重分布）
3. 添加适当的思考时间（wait_time）
4. 包含成功和失败的断言
5. 添加自定义指标收集
6. 类型注解和注释完整

只输出Python代码，不要其他解释。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def generate_test_strategy(scenario: str) -> str:
    """Generate performance test strategy."""
    prompt = f"""你是一个资深性能测试架构师。请为以下场景设计完整的性能测试策略。

业务场景：
{scenario}

要求：
1. 测试目标（吞吐量、响应时间、资源利用率）
2. 测试类型（负载测试、压力测试、稳定性测试、容量测试）
3. 阶梯加压方案（并发数、持续时间、步长）
4. 监控指标（应用层、系统层、数据库层）
5. 通过/失败标准（SLA）
6. 风险点和注意事项

用结构化的Markdown格式输出。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def analyze_perf_results(metrics: str) -> str:
    """Analyze performance test results."""
    prompt = f"""你是一个资深性能测试专家。请分析以下压测结果，找出瓶颈并给出优化建议。

压测数据：
{metrics}

要求：
1. 结果概述：整体表现如何
2. 瓶颈识别：哪个环节可能是瓶颈（应用服务器、数据库、网络、缓存）
3. 优化建议：按优先级排序，每个建议说明预期效果
4. 下一步测试建议：还需要补充哪些测试来验证

用结构化的Markdown格式输出。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def main():
    parser = argparse.ArgumentParser(description="Performance Test Assistant")
    parser.add_argument("--api", type=str, help="接口信息描述")
    parser.add_argument("--users", type=int, default=100, help="并发用户数")
    parser.add_argument("--duration", type=str, default="60s", help="压测时长")
    parser.add_argument("--strategy", type=str, help="生成测试策略")
    parser.add_argument("--analyze", type=str, help="分析压测结果")
    
    args = parser.parse_args()
    
    if args.api:
        print(generate_locust_script(args.api, args.users, args.duration))
    elif args.strategy:
        print(generate_test_strategy(args.strategy))
    elif args.analyze:
        print(analyze_perf_results(args.analyze))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
