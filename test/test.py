import subprocess
import json
import os


def load_config(config_path: str = "config.json") -> dict:
    """
    設定ファイルを読み込む。

    Args:
        config_path (str): 設定ファイルのパス

    Returns:
        dict: 設定内容を含む辞書
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"設定ファイルが見つかりません: {config_path}")

    with open(config_path, "r") as file:
        config = json.load(file)
    return config


def select_problem(config: dict) -> int:
    """
    テストを行う問題番号を標準入力で受け取る。
    バリデーションを行い、不正な場合は再度入力を受け取る。

    Args:
        config (dict): 設定内容を含む辞書

    Returns:
        int: 選択された問題番号
    """
    expected_problem_num = list(range(1, config["problem_count"] + 1))
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


def summarize_output(output: str, max_lines: int, max_length: int) -> str:
    """
    長い入出力を要約して表示するための関数。
    各行の長さが指定された最大長を超える場合、最初と最後の部分を表示する。
    行数が指定された最大行数を超える場合、最初の行と最後の行を表示する。

    Args:
        output (str): 出力テキスト
        max_lines (int): 最大行数
        max_length (int): 各行の最大長

    Returns:
        str: 要約された出力テキスト
    """
    lines = output.splitlines()

    def shorten_line(line: str, max_length: int) -> str:
        if len(line) > max_length:
            return f"{line[:max_length//2]}\033[90m...skip {len(line) - max_length} chars...\033[0m{line[-max_length//2:]}"
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


def run_test(problem_num: int, config: dict) -> int:
    """
    テストを行う。
    正解数、テストケースごとの結果を格納したリストを返す。

    Args:
        problem_num (int): 問題番号
        config (dict): 設定内容を含む辞書

    Returns:
        int: 正解数
    """
    AC_num = 0
    test_case_count = config["test_case_count"]
    input_directory = config["directories"]["input"]
    output_directory = config["directories"]["output"]
    problem_directory = "problem"

    for test_number in range(1, test_case_count + 1):
        with open(
            f"{input_directory}/{problem_num:02}/in{test_number:02}.txt", "r"
        ) as file:
            test_input = file.read()

        with open(
            f"{output_directory}/{problem_num:02}/out{test_number:02}.txt", "r"
        ) as file:
            expected_output = file.read().strip()

        process = subprocess.Popen(
            ["python", f"{problem_directory}/problem{problem_num:02}.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            stdout, stderr = process.communicate(
                input=test_input, timeout=config["limits"]["time_limit"]
            )
            passed = stdout.strip() == expected_output
            if stderr:
                result = f"\033[91mRE\033[0m\n{summarize_output(stderr, config['limits']['max_line_length'], config['limits']['max_input_length'])}\n"
            elif passed:
                result = "\033[92mAC\033[0m\n"
                AC_num += 1
            else:
                result = (
                    f"\033[91mWA\033[0m\n"
                    f"\033[96m[in]\033[0m:\n{summarize_output(test_input, config['limits']['max_line_length'], config['limits']['max_input_length'])}\n"
                    f"\033[96m[out]\033[0m:\n{summarize_output(stdout, config['limits']['max_line_length'], config['limits']['max_input_length'])}\n"
                    f"\033[96m[expected_out]\033[0m:\n{summarize_output(expected_output, config['limits']['max_line_length'], config['limits']['max_input_length'])}\n"
                )
        except subprocess.TimeoutExpired:
            process.kill()
            result = "\033[91mTLE\033[0m\n"

        print(f"[テストケース{test_number}]: {result}")

    return AC_num


def main():
    config = load_config()
    problem_num = select_problem(config)
    AC_num = run_test(problem_num, config)
    if AC_num == config["test_case_count"]:
        print("\033[92m全てのテストケースでACです。\033[0m")
    else:
        print("\033[91m不正解なテストケースがあります。\033[0m")
        print(f"ACした数: {AC_num}/{config['test_case_count']}")


if __name__ == "__main__":
    main()
