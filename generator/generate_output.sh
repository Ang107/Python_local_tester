#各自パスの変更が必要
cd 


for problem_num in `seq 1 5`;
    do
    for test_num in `seq 1 10`;
        do
            problem_num_0=$(printf "%02d\n" "${problem_num}")
            test_num_0=$(printf "%02d\n" "${test_num}")

            pypy3  "answer/ans${problem_num_0}.py" < test/in/${problem_num_0}/in${test_num_0}.txt > test/out/${problem_num_0}/out${test_num_0}.txt

        done
    done

