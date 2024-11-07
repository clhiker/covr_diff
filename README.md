# covr_diff

## z3 调用
./z3 /home/clhiker/seeds/1.smt2

## gcovr 用法
### HTML 报告
gcovr -r . --html --html-details -o coverage_report.html

### JSON报告
分支
gcovr -r . --branches --json -o /home/clhiker/report/coverage-report.json
函数
gcovr -r . --functions-only --json -o /home/clhiker/func-json-report/coverage-report.json


## gcno 和 gcda
find . -name "*.gcno"
find . -name "*.gcda"
find . -name "*.gcda" -exec rm -f {} +      # 清理gcda