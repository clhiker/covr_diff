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
    def run_cases_first(self):
        for i in range(self.seed_num):
            print('run z3')
            subprocess.run([self.z3_path, self.seed_path + str(i) + '.smt2'])
            print('run gcovr')
            subprocess.run(
                ['gcovr', '-r', '.', '-d', '-j', '8', '--json', '-o', self.z3_report_path + '/' + str(i) + '.json'],
                cwd=self.z3_build_path)

    # def run_cases_other(self):
    #     for i in range(self.seed_num):
    #         print('run cvc5')
    #         subprocess.run([self.cvc5_path, self.seed_path + str(i) + '.smt2'])
    #         print('run gcovr')
    #         subprocess.run(
    #             ['gcovr', '-r', '.', '-d', '-j', '8', '--json', '-o', self.cvc5_report_path + '/' + str(i) + '.json'],
    #             cwd=self.cvc5_build_path)

    def run_cases_other(self):
        for i in range(self.seed_num):
            print('run cvc5')
            subprocess.run([self.cvc5_path, self.seed_path + str(i) + '.smt2'])
            print('run gcovr')
            subprocess.run(
                ['fastcov', '-o', self.cvc5_report_path + '/' + str(i) + '.json'],
                cwd=self.cvc5_build_path)

    # 收集分支信息，将相同分支的用例进行规约
    def statue_cases(self):
        z3_cover_all = {}
        for name in os.listdir(self.z3_report_path):
            path = os.path.join(self.z3_report_path, name)
            with open(path, 'r') as f:
                z3_cover_all[name] = json.load(f)
        z3_cover_info = {}
        for key, val in z3_cover_all.items():
            info = set()
            files = val['files']
            for file_dict in files:
                funcs = file_dict['functions']
                filename = file_dict['file']
                for func in funcs:
                    if func['execution_count'] > 0:
                        info.add(filename + ' ' + func['demangled_name'])
            sorted_info_list = sorted(info)
            concatenated_info = ''.join(sorted_info_list)
            md5_hash = hashlib.md5(concatenated_info.encode('utf-8')).hexdigest()
            z3_cover_info[key] = md5_hash

        for key, val in z3_cover_info.items():
            if val not in self.z3_group_info:
                self.z3_group_info[val] = [key]
            else:
                self.z3_group_info[val].append(key)

        cvc5_cover_all = {}
        for name in os.listdir(self.cvc5_report_path):
            path = os.path.join(self.cvc5_report_path, name)
            with open(path, 'r') as f:
                cvc5_cover_all[name] = json.load(f)
        cvc5_cover_info = {}
        for key, val in cvc5_cover_all.items():
            info = set()
            files = val['files']
            for file_dict in files:
                funcs = file_dict['functions']
                filename = file_dict['file']
                for func in funcs:
                    if func['execution_count'] > 0:
                        info.add(filename + ' ' + func['demangled_name'])
            sorted_info_list = sorted(info)
            concatenated_info = ''.join(sorted_info_list)
            md5_hash = hashlib.md5(concatenated_info.encode('utf-8')).hexdigest()
            cvc5_cover_info[key] = md5_hash

        for key, val in cvc5_cover_info.items():
            if val not in self.cvc5_group_info:
                self.cvc5_group_info[val] = [key]
            else:
                self.cvc5_group_info[val].append(key)

        pass

    def statue_case_from_fastcov(self):
        cvc5_cover_all = {}
        for name in os.listdir(self.cvc5_report_path):
            path = os.path.join(self.cvc5_report_path, name)
            with open(path, 'r') as f:
                cvc5_cover_all[name] = json.load(f)
        cvc5_cover_info = {}
        for key, val in cvc5_cover_all.items():
            info = set()
            sources = res['sources']
            for file, file_info in sources.items():
                funcs = file_info['']['functions']
                for func_name, func_info in funcs.items():
                    if func_info['execution_count'] > 0:
                        info.add(file + ' ' + func_name)
            sorted_info_list = sorted(info)
            concatenated_info = ''.join(sorted_info_list)
            md5_hash = hashlib.md5(concatenated_info.encode('utf-8')).hexdigest()
            cvc5_cover_info[key] = md5_hash

        for key, val in cvc5_cover_info.items():
            if val not in self.cvc5_group_info:
                self.cvc5_group_info[val] = [key]
            else:
                self.cvc5_group_info[val].append(key)

    # 将规约后的用例运行在第二个目标实现上面
    def run_cases_second(self):
        for val in self.z3_group_info.values():
            for cover_name in val:
                name = cover_name[:cover_name.rfind('.')]
                seed_path = os.path.join(self.seed_path, name + '.smt2')
                print(seed_path)
        pass

    def run(self):
        # self.fuzzing_cases()
        self.run_cases_first()
        # self.statue_cases()
        # self.run_cases_other()
        pass


if __name__ == '__main__':
    covr_diff = COVR_DIFF()
    covr_diff.run()