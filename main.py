import hashlib
import json
import os
import subprocess
from fileinput import filename


class COVR_DIFF:
    def __init__(self):
        self.seed_path = '/home/clhiker/seeds/'
        self.seed_num = 100
        self.z3_build_path = '/home/clhiker/z3/build'
        self.z3_path = '/home/clhiker/z3/build/z3'
        self.cvc5_build_path = '/home/clhiker/cvc5/build'
        self.cvc5_path = '/home/clhiker/cvc5/build/bin/cvc5'
        self.z3_report_path = '/home/clhiker/z3-report'
        self.cvc5_report_path = '/home/clhiker/cvc5-report'
        self.z3_func_class_path = '/home/clhiker/cover-res/z3-func.json'
        self.cvc5_func_class_path = '/home/clhiker/cover-res/cvc5-func.json'
        self.z3_branch_class_path = '/home/clhiker/cover-res/z3-branch.json'
        self.cvc5_branch_class_path = '/home/clhiker/cover-res/cvc5-branch.json'

        self.z3_group_info = dict()
        self.cvc5_group_info = dict()
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
    def run_cases(self):
        for i in range(self.seed_num):
            print('run z3')
            subprocess.run([self.z3_path, self.seed_path + str(i) + '.smt2'])
            print('run fastcov')
            subprocess.run(['fastcov', '-j', '8', '-o', self.z3_report_path + '/' + str(i) + '.json'], cwd=self.z3_build_path)
            subprocess.run(['fastcov', '-z'], cwd=self.z3_build_path)

        for i in range(self.seed_num):
            print('run cvc5')
            subprocess.run([self.cvc5_path, self.seed_path + str(i) + '.smt2'])
            print('run fastcov')
            subprocess.run(['fastcov', '-j', '8', '-o', self.cvc5_report_path + '/' + str(i) + '.json'], cwd=self.cvc5_build_path)
            subprocess.run(['fastcov', '-z'], cwd=self.cvc5_build_path)

    # 收集分支信息，将相同分支的用例进行规约
    def statue_cases(self):
        self.statue_func(self.z3_report_path, self.z3_branch_class_path)
        self.statue_func(self.cvc5_report_path, self.cvc5_branch_class_path)

    def statue_func(self, report_path, class_path):
        cover_all = {}
        for name in os.listdir(report_path):
            path = os.path.join(report_path, name)
            with open(path, 'r') as f:
                cover_all[name] = json.load(f)
        cover_info = {}
        for key, val in cover_all.items():
            info = set()
            sources = val['sources']
            for file, file_info in sources.items():
                funcs = file_info['']['functions']
                for func_name, func_info in funcs.items():
                    if func_info['execution_count'] > 0:
                        info.add(file + ' ' + func_name)
            sorted_info_list = sorted(info)
            concatenated_info = ''.join(sorted_info_list)
            md5_hash = hashlib.md5(concatenated_info.encode('utf-8')).hexdigest()
            cover_info[key] = md5_hash

        group_info = dict()
        for key, val in cover_info.items():
            if val not in group_info:
                group_info[val] = [key]
            else:
                group_info[val].append(key)
        with open(class_path, 'w') as f:
            json.dump(group_info, f)

    def statue_branch(self, report_path, class_path):
        cover_all = {}
        for name in os.listdir(report_path):
            path = os.path.join(report_path, name)
            with open(path, 'r') as f:
                cover_all[name] = json.load(f)
        cover_info = {}
        for key, val in cover_all.items():
            info = set()
            sources = val['sources']
            for file, file_info in sources.items():
                funcs = file_info['']['functions']
                for func_name, func_info in funcs.items():
                    if func_info['execution_count'] > 0:
                        info.add(file + ' ' + func_name)
            sorted_info_list = sorted(info)
            concatenated_info = ''.join(sorted_info_list)
            md5_hash = hashlib.md5(concatenated_info.encode('utf-8')).hexdigest()
            cover_info[key] = md5_hash

        group_info = dict()
        for key, val in cover_info.items():
            if val not in group_info:
                group_info[val] = [key]
            else:
                group_info[val].append(key)
        with open(class_path, 'w') as f:
            json.dump(group_info, f)

    # 将规约后的用例运行在第二个目标实现上面
    def run_cases_second(self):
        for val in self.z3_group_info.values():
            for cover_name in val:
                name = cover_name[:cover_name.rfind('.')]
                seed_path = os.path.join(self.seed_path,  name + '.smt2')
                print(seed_path)

    def run(self):
        self.fuzzing_cases()
        self.run_cases()
        self.statue_cases()
        pass


if __name__ == '__main__':
    covr_diff = COVR_DIFF()
    covr_diff.run()