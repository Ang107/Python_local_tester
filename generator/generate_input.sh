#!/bin/bash

# 設定ファイルの読み込み
CONFIG_FILE="config.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "設定ファイルが見つかりません: $CONFIG_FILE"
    exit 1
fi

# 設定ファイルから変数を読み込み
PROBLEM_COUNT=$(jq -r '.problem_count' "$CONFIG_FILE")
TEST_CASE_COUNT=$(jq -r '.test_case_count' "$CONFIG_FILE")
CURRENT_DIRECTORY=$(jq -r '.directories.current' "$CONFIG_FILE")
INPUT_DIRECTORY=$(jq -r '.directories.input' "$CONFIG_FILE")
GENERATOR_DIRECTORY=$(jq -r '.directories.generator' "$CONFIG_FILE")

# カレントディレクトリの存在確認
if [[ ! -d "$CURRENT_DIRECTORY" ]]; then
    echo "ディレクトリが見つかりません: $CURRENT_DIRECTORY"
    exit 1
fi
cd "$CURRENT_DIRECTORY"

# 入力ファイルの生成
for problem_num in $(seq 1 "$PROBLEM_COUNT"); do
    for test_num in $(seq 1 "$TEST_CASE_COUNT"); do
        problem_num_with_0=$(printf "%02d\n" "${problem_num}")
        test_num_with_0=$(printf "%02d\n" "${test_num}")

        # 必要なディレクトリが存在しない場合は作成
        mkdir -p "${INPUT_DIRECTORY}/${problem_num_with_0}"

        # 入力ファイルの生成
        pypy3 "${GENERATOR_DIRECTORY}/generate_input${problem_num_with_0}.py" > "${INPUT_DIRECTORY}/${problem_num_with_0}/in${test_num_with_0}.txt"
        if [[ $? -ne 0 ]]; then
            echo "入力ファイル生成中にエラーが発生しました: problem ${problem_num_with_0}, test case ${test_num_with_0}"
            exit 1
        fi
    done
done

echo "すべての入力ファイルが正常に生成されました。"
