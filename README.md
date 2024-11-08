# covr_diff

## z3 构建

### CMakeList.txt 
OPTION(ENABLE_GCOV "Enable gcov (debug, Linux builds only)" OFF)

IF (ENABLE_GCOV AND NOT WIN32 AND NOT APPLE)
  SET(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fprofile-arcs -ftest-coverage")
  SET(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -fprofile-arcs -ftest-coverage")
  SET(CMAKE_EXE_LINKER_FLAGS_DEBUG "${CMAKE_EXE_LINKER_FLAGS_DEBUG} -fprofile-arcs -ftest-coverage -lgcov")
ENDIF()

### cmake 构建
cmake .. -DCMAKE_BUILD_TYPE=Debug -DENABLE_GCOV=1

## z3 调用
./z3 /home/clhiker/seeds/1.smt2

## gcovr 用法
### HTML 报告
gcovr -r . --html --html-details -o coverage_report.html

### JSON报告
分支
gcovr -r . --branches --json -o /home/clhiker/report/coverage-report.json


## gcno 和 gcda
find . -name "*.gcno"
find . -name "*.gcda"
find . -name "*.gcda" -exec rm -f {} +      # 清理gcda，gcovr -d 默认会删除