import random
import itertools
from typing import List, Dict, Tuple

class LogicalPuzzleGenerator:
    def __init__(self, 
                 n_people: int = 3,
                 n_doors: int = 2,
                 n_truthful: int = 1,
                 max_attempts: int = 100):
        """
        唯一解逻辑谜题生成器
        
        参数：
        n_people: 总人数
        n_doors: 门的总数
        n_truthful: 说真话者数量
        max_attempts: 最大生成尝试次数
        """
        self.n_people = n_people
        self.n_doors = n_doors
        self.n_truthful = n_truthful
        self.max_attempts = max_attempts
        self.people = [f"P{i+1}" for i in range(n_people)]
        
    def generate_problem(self) -> Tuple[Dict, Dict]:
        """
        生成具有唯一解的问题
        
        返回：
        (problem, solution) 元组
        problem格式：{
            "statements": {人: [陈述列表]},
            "constraints": ["有2人说真话"]
        }
        solution格式：{
            "truthful": [说真话者列表],
            "correct_door": int
        }
        """
        for _ in range(self.max_attempts):
            # 步骤1：预设正确答案
            solution = self._preset_solution()
            
            # 步骤2：生成逻辑约束
            constraints = self._generate_constraints(solution)
            
            # 步骤3：构建陈述系统
            statements = self._build_statements(solution, constraints)
            
            # 步骤4：验证唯一解
            if self._validate_uniqueness(statements, solution):
                problem = {
                    "statements": statements,
                    "constraints": [
                        f"有{self.n_truthful}人说真话",
                        "只有一扇正确的门"
                    ]
                }
                return problem, solution
        
        raise RuntimeError("无法在尝试次数内生成有效问题")

    def _preset_solution(self) -> Dict:
        """ 预设正确答案 """
        return {
            "truthful": random.sample(self.people, self.n_truthful),
            "correct_door": random.randint(1, self.n_doors)
        }
    
    def _generate_constraints(self, solution: Dict) -> List[str]:
        """ 生成用于确保唯一解的逻辑约束 """
        constraints = []
        correct_door = solution["correct_door"]
        
        # 添加否定约束（确保其他门不可能正确）
        for door in range(1, self.n_doors+1):
            if door != correct_door:
                constraints.append(f"门{door}不正确")
        
        # 添加身份关联约束（示例：至少一个真话者指认正确门）
        constraints.append(f"至少一人直接指认门{correct_door}")
        
        return constraints
    
    def _build_statements(self, 
                         solution: Dict,
                         constraints: List[str]) -> Dict[str, List[str]]:
        """ 构建满足约束的陈述系统 """
        statements = {}
        correct_door = solution["correct_door"]
        truthful_people = solution["truthful"]
        
        # 陈述模板库
        templates = {
            "direct": ["门{}正确", "门{}不正确"],
            "conditional": [
                "如果门{}正确，则门{}不正确",
                "门{}正确当且仅当门{}不正确"
            ],
            "quantified": [
                "至少有一个正确门",
                "所有偶数门都不正确"
            ]
        }
        
        for person in self.people:
            stmts = []
            is_truthful = person in truthful_people
            
            # 生成3条陈述（数量可调）
            for _ in range(3):
                # 随机选择模板类型
                template_type = random.choice(["direct", "conditional", "quantified"])
                
                if template_type == "direct":
                    door = random.randint(1, self.n_doors)
                    truth_value = (door == correct_door)
                    if not is_truthful:
                        truth_value = not truth_value
                    stmts.append(templates["direct"][int(truth_value)].format(door))
                
                elif template_type == "conditional":
                    d1, d2 = random.sample(range(1, self.n_doors+1), 2)
                    actual_relation = (d1 == correct_door) and (d2 != correct_door)
                    if is_truthful:
                        stmt = templates["conditional"][0].format(d1, d2) if actual_relation \
                               else templates["conditional"][1].format(d1, d2)
                    else:
                        stmt = templates["conditional"][0].format(d2, d1) if not actual_relation \
                               else templates["conditional"][1].format(d2, d1)
                    stmts.append(stmt)
                
                elif template_type == "quantified":
                    # 处理量化陈述的逻辑
                    pass  # 简化实现
                    
            statements[person] = stmts
        
        return statements
    
    def _validate_uniqueness(self,
                            statements: Dict[str, List[str]],
                            expected_solution: Dict) -> bool:
        """ 验证答案唯一性 """
        # 穷举所有可能的解
        solutions = []
        
        # 遍历所有可能的正确门
        for candidate_door in range(1, self.n_doors+1):
            # 遍历所有可能的真话者组合
            for truthful_comb in itertools.combinations(self.people, self.n_truthful):
                valid = True
                
                # 验证每个陈述是否符合假设
                for person, stmts in statements.items():
                    is_truthful = person in truthful_comb
                    for stmt in stmts:
                        # 此处需要实现陈述验证逻辑（简化版）
                        truth_value = self._evaluate_statement(stmt, candidate_door)
                        if is_truthful != truth_value:
                            valid = False
                            break
                    if not valid:
                        break
                
                if valid:
                    solutions.append({
                        "truthful": truthful_comb,
                        "correct_door": candidate_door
                    })
        
        # 检查是否只有预设解有效
        return len(solutions) == 1 and solutions[0] == expected_solution
    
    def _evaluate_statement(self, stmt: str, correct_door: int) -> bool:
        """ 简化的陈述验证逻辑 """
        if "正确" in stmt:
            door = int(stmt[1])
            return door == correct_door
        # 更复杂的逻辑需要扩展此方法
        return False

# 使用示例
if __name__ == "__main__":
    generator = LogicalPuzzleGenerator(n_people=3, n_doors=3)
    problem, solution = generator.generate_problem()
    
    print("=== 生成问题 ===")
    for person, stmts in problem["statements"].items():
        print(f"{person}:")
        for stmt in stmts:
            print(f" - {stmt}")
    print("\n约束条件:")
    for c in problem["constraints"]:
        print(f" - {c}")
    
    print("\n=== 预设答案 ===")
    print(f"正确门: 门{solution['correct_door']}")
    print(f"说真话者: {', '.join(solution['truthful'])}")