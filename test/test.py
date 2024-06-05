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


def summarize_output(output: str, max_lines: int = 10, max_length: int = 50) -> str:
    """
    長い入出力を要約して表示するための関数。
    各行の長さが指定された最大長を超える場合、最初と最後の5文字を表示する。
    行数が指定された最大行数を超える場合、最初の25行と最後の25行を表示する。
    """
    lines = output.splitlines()

    def shorten_line(line: str, max_length: int) -> str:
        if len(line) > max_length:
            return f"{line[:max_length//2]}\033[90m...skip {len(line) - max_length}chars...\033[0m{line[-max_length//2:]}"
        return line

    if len(lines) > max_lines:
        summarized_lines = (
            [shorten_line(line, max_length) for line in lines[: max_lines // 2]]
            + [f"\033[90m... skip {len(lines) - max_lines} lines ...\033[0m"]
            + [shorten_line(line, max_length) for line in lines[-max_lines // 2 :]]
        )
    else:
        summarized_lines = [shorten_line(line, max_length) for line in lines]

    return "\n".join(summarized_lines)


def run_test(problem_num: int, timeout: float) -> tuple[int, int, list[str]]:
    """
    テストを行う。
    正解数、テストケースごとの結果を格納したリストを返す。
    """
    AC_num = 0

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

        try:
            # 標準入力にテスト入力を渡し、標準出力をキャプチャ
            stdout, stderr = process.communicate(input=test_input, timeout=timeout)
            passed = stdout.strip() == expected_output
            if stderr:
                result = f"\033[91mRE\033[0m\n{summarize_output(stderr)}\n"  # 赤色
            elif passed:
                result = "\033[92mAC\033[0m\n"  # 緑色
                AC_num += 1
            else:
                result = (
                    f"\033[91mWA\033[0m\n"
                    f"\033[96m[in]\033[0m:\n{summarize_output(test_input)}\n"
                    f"\033[96m[out]\033[0m:\n{summarize_output(stdout)}\n"
                    f"\033[96m[expected_out]\033[0m:\n{summarize_output(expected_output)}\n"
                )  # 赤色 + シアン色
        except subprocess.TimeoutExpired:
            process.kill()
            result = "\033[91mTLE\033[0m\n"  # 赤色

        print(f"[テストケース{test_number}]: {result}")

    return AC_num


def main():
    problem_num = select_problem()
    timeout = 3  # タイムアウト時間を秒で設定
    AC_num = run_test(problem_num, timeout)
    if AC_num == 10:
        print("\033[92m全てのテストケースでACです。\033[0m")  # 緑色
    else:
        print("\033[91m不正解なテストケースがあります。\033[0m")  # 赤色
        print(f"ACした数: {AC_num}/10")


if __name__ == "__main__":
    main()
