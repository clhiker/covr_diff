import random
from z3 import *
import os

# 设置 Z3 求解器
solver = Solver()

# 生成随机的 SMT 公式
def generate_random_smt_formula(num_formulas=100, max_depth=5):
    variables = [Bool(f"x{i}") for i in range(1, 11)]  # 创建 10 个布尔变量 x1, x2, ..., x10
    operators = ['And', 'Or', 'Not', 'Implies', 'Xor']

    def generate_formula(depth=0):
        # 限制公式的深度，防止公式过于复杂
        if depth >= max_depth or random.random() > 0.7:
            return random.choice(variables)  # 随机选择一个布尔变量

        op = random.choice(operators)
        if op == 'Not':
            return Not(generate_formula(depth + 1))  # 生成一个 'Not' 操作
        elif op == 'And':
            return And(generate_formula(depth + 1), generate_formula(depth + 1))  # 生成一个 'And' 操作
        elif op == 'Or':
            return Or(generate_formula(depth + 1), generate_formula(depth + 1))  # 生成一个 'Or' 操作
        elif op == 'Implies':
            left = generate_formula(depth + 1)
            right = generate_formula(depth + 1)
            return Implies(left, right)  # 使用 Z3 内部的 Implies
        elif op == 'Xor':
            return Xor(generate_formula(depth + 1), generate_formula(depth + 1))  # 生成一个 'Xor' 操作

    formulas = [generate_formula() for _ in range(num_formulas)]
    return formulas

# 将 Z3 公式转换为 SMT-LIB 格式的字符串
def smt_formula_to_smtlib(formula):
    if is_not(formula):
        return f"(not {smt_formula_to_smtlib(formula.arg(0))})"
    elif is_and(formula):
        return f"(and {smt_formula_to_smtlib(formula.arg(0))} {smt_formula_to_smtlib(formula.arg(1))})"
    elif is_or(formula):
        return f"(or {smt_formula_to_smtlib(formula.arg(0))} {smt_formula_to_smtlib(formula.arg(1))})"
    elif is_implies(formula):
        return f"(=> {smt_formula_to_smtlib(formula.arg(0))} {smt_formula_to_smtlib(formula.arg(1))})"
    elif formula.decl().name() == "xor":
        return f"(xor {smt_formula_to_smtlib(formula.arg(0))} {smt_formula_to_smtlib(formula.arg(1))})"
    else:
        return str(formula)  # 对于变量，直接返回其字符串形式

# 保存随机生成的公式到文件
def save_formulas_to_files(formulas, output_dir="/home/clhiker/smt_random"):
    # 创建输出目录（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 确保所有的布尔变量 x1, x2, ..., x10 被声明
    variable_declarations = [
        f"(declare-fun x{i} () Bool)" for i in range(1, 11)
    ]

    # 保存每个公式到独立的文件
    for i, formula in enumerate(formulas):
        formula_smtlib = smt_formula_to_smtlib(formula)
        filename = os.path.join(output_dir, f"sr{i + 1}.smt2")
        with open(filename, 'w') as f:
            # 写入逻辑和变量声明
            f.write("(set-logic QF_BV)\n")
            f.write("\n".join(variable_declarations) + "\n")  # 变量声明
            f.write(f"(assert {formula_smtlib})\n")  # 公式本身
            f.write("(check-sat)\n")  # 检查可满足性
        print(f"Formula {i + 1} saved to {filename}")

# 随机生成 100 个 SMT 公式
random_smt_formulas = generate_random_smt_formula(100)

# 保存这些公式到文件
save_formulas_to_files(random_smt_formulas)
