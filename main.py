import json
import os
import subprocess

class COVR_DIFF:
    def __init__(self):
        self.seed_path = '/home/clhiker/seeds/'
        self.seed_num = 10
        self.z3_build_path = '/home/clhiker/z3/build'
        self.z3_path = '/home/clhiker/z3/build/z3'
        self.covr_report_path = '/home/clhiker/report'
        if not os.path.exists(self.seed_path):
            os.mkdir(self.seed_path)
        pass

    # 构建包含覆盖率信息的对象
    def build_cov_target(self):
        pass

    # 使用fuzzer工具生成大量的测试用例/1k一分类
    def fuzzing_cases(self):
        for i in range(self.seed_num):
            os.system('smtfuzz' + ' >> ' + self.seed_path + str(i) + '.smt2')

    # 将生成的用例运行在第一个目标对象上面
    def run_cases_first(self):
        for i in range(self.seed_num):
            print('run z3')
            subprocess.run([self.z3_path, self.seed_path + str(i) + '.smt2'])
            print('run gcovr')
            subprocess.run(
                ['gcovr', '-r', '.', '--branches', '--json', '-o', self.covr_report_path + '/' + str(i) + '.json'],
                cwd=self.z3_build_path)
            print('clear gcda info')
            subprocess.run(['find', '.', '-name', '*.gcda', '-exec', 'rm', '-f', '{}', '+'], cwd=self.z3_build_path)
        pass

    # 收集分支信息，将相同分支的用例进行规约
    def statue_cases(self):
        covr_info = {}
        for name in os.listdir(self.covr_report_path):
            path = os.path.join(self.covr_report_path, name)
            with open(path, 'r') as f:
                covr_info[name] = json.load(f)

        print(covr_info)

    # 将规约后的用例运行在第二个目标实现上面
    def run_cases_second(self):
        pass

    def run(self):
        # self.fuzzing_cases()
        # self.run_cases_first()
        self.statue_cases()
        pass


if __name__ == '__main__':
    covr_diff = COVR_DIFF()
    covr_diff.run()