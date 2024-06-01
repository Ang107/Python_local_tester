#各自パスの変更が必要
cd 


for problem_num in `seq 1 5`;
    do
    for test_num in `seq 5 10`;
        do
            problem_num_0=$(printf "%02d\n" "${problem_num}")
            test_num_0=$(printf "%02d\n" "${test_num}")

            pypy3  "generator/generate_input${problem_num_0}.py" > test/in/${problem_num_0}/in${test_num_0}.txt

        done
    done