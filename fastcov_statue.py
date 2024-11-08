import json

info = set()
with open('/home/clhiker/z3-report/1.json', 'r') as f:
    res = json.load(f)
    sources = res['sources']
    for file, file_info in sources.items():
        funcs = file_info['']['functions']
        for func_name, func_info in funcs.items():
            if func_info['execution_count'] > 0:
                info.add(file + ' ' + func_name)
    sorted_info_list = sorted(info)
    concatenated_info = ''.join(sorted_info_list)