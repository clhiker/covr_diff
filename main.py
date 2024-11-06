

class COVR_DIFF:
    def __init__(self):
        pass

    # 构建包含覆盖率信息的对象
    def build_cov_target(self):
        pass

    # 使用fuzzer工具生成大量的测试用例/1k一分类
    def fuzzing_cases(self):
        pass

    # 将生成的用例运行在第一个目标对象上面
    def run_cases_first(self):
        pass

    # 收集分支信息，将相同分支的用例进行规约
    def statue_cases(self):
        pass

    # 将规约后的用例运行在第二个目标实现上面
    def run_cases_second(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    covr_diff = COVR_DIFF()
    covr_diff.run()