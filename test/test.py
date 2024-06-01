import subprocess


def select_problem() -> int:
    """
    テストを行う問題番号を標準入力で受け取る。
    バリデーションを行い、不正な場合は再度入力を受け取る。
    """
    # 適切な問題番号のリストを指定
    expected_problem_num = [1, 2, 3, 4, 5]
    while True:
        try:
            problem_num = int(
                input(
                    f"テストを行う問題番号{expected_problem_num}を入力してください。: "
                )
            )
            if problem_num in expected_problem_num:
                break
            else:
                print(f"入力が不正です。適切な入力の一覧: {expected_problem_num}")
        except ValueError:
            print(f"入力が不正です。適切な入力の一覧: {expected_problem_num}")
    return problem_num


def run_test(problem_num: int) -> tuple[int, int, list[str]]:
    """
    テストを行う。
    正解数、テストケースごとの結果を格納したリストを返す。
    """
    AC_num = 0
    test_result = []
    # テストケースは1 ~ 10 の10個で固定
    for test_number in range(1, 11):
        # 入力を読み込む
        with open(f"test/in/{problem_num:02}/in{test_number:02}.txt", "r") as file:
            test_input = file.read()

        # 適切な出力を読み込む
        with open(f"test/out/{problem_num:02}/out{test_number:02}.txt", "r") as file:
            expected_output = file.read().strip()

        # 他人のコードを実行
        process = subprocess.Popen(
            ["python", f"problem/problem{problem_num:02}.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # 標準入力にテスト入力を渡し、標準出力をキャプチャ
        stdout, stderr = process.communicate(input=test_input)

        passed = stdout.strip() == expected_output
        if stderr:
            test_result.append(f"実行時エラー: {stderr}\n")
        elif passed:
            test_result.append("AC\n")
            AC_num += 1
        else:
            test_result.append(
                f"WA\nin:\n{test_input}out: {stdout}\nexpected_out: {expected_output}\n"
            )
    return AC_num, test_result


def main():
    problem_num = select_problem()
    AC_num, test_result = run_test(problem_num)
    if AC_num == 10:
        print("全てのテストケースでACです。")
    else:
        print("不正解なケースがあります。")
        print(f"ACした数: {AC_num}/10")
        for i, result in enumerate(test_result):
            print(f"テストケース{i+1}: {result}")


if __name__ == "__main__":
    main()
