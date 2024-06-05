# Python_local_tester

## 概要

- このツールは、ローカル環境でPythonコードの簡単なテストを実行するための一式です。
- Windows, PowerShellで動作を確認しています。
- pythonコマンドが使用可能である必要があるため、Pythonのインストール、PATHの設定が必要です。

### 使用方法

#### 解答者向け

1. `problem` フォルダ内のPythonファイルに追記する形で問題を解いてください。
2. 問題を解けた場合は、`test/test.py` を実行し、テストしたい問題番号を入力してください。
3. テストの結果が出力されます。
4. 「全てのテストケースでACです。」と表示されればその問題は正解です。そうでない場合は、不正解となるテストケースや、エラー、時間超過となるケースを参考に、コードを修正しましょう。

#### 問題作成者向け

1. 各フォルダ内の `info.txt` に従ってファイルを作成、配置してください。
2. 必要に応じて、`generate_input.sh` および `generate_output.sh` を編集してください。

### 作業ディレクトリに関する注意事項

`test/test.py`を実行する際は、必ず**Python_local_tester**フォルダを作業ディレクトリ（カレントディレクトリ）として実行してください。これにより、スクリプトが正しいファイルパスを参照し、テストケースを正しく読み込むことができます。

#### 例：

1. PowerShellを開きます。
2. **Python_local_tester**フォルダに移動します。
3. `test/test.py`を実行します。
    ```powershell
    python .\test\test.py
    ```

この手順を守ることで、スクリプトが正しく動作し、問題なくテストを実行することができます。

### 設定ファイル (`config.json`)

このファイルは、テスト環境の設定を定義します。

```json
{
    "problem_count": 5,
    "test_case_count": 10,
    "directories": {
        "current": "/path/to/current/directory",
        "input": "test/in",
        "output": "test/out",
        "generator": "generator",
        "answer": "answer"
    },
    "limits": {
        "max_input_length": 50,
        "max_line_length": 10,
        "time_limit": 3.0
    }
}
```
- `problem_count`: 問題の総数
- `test_case_count`: 各問題に対するテストケースの総数
- `directories`: 各種ディレクトリのパス
  - `current`: カレントディレクトリのパス
  - `input`: 入力ファイルを保存するディレクトリのパス
  - `output`: 出力ファイルを保存するディレクトリのパス
  - `generator`: 入力生成スクリプトのディレクトリのパス
  - `answer`: 想定解スクリプトのディレクトリのパス
- `limits`: 各種制限
  - `max_input_length`: 入力の最大長
  - `max_line_length`: 各行の最大長
  - `time_limit`: 各テストケースのタイムリミット（秒）

### フォルダ構成の例

問題数が5、テストケース数が10の場合の例として、空ファイルを配置しています。必要に応じて、削除・追加してください。
