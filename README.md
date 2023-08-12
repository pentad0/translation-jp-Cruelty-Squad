# Cruelty Squad
今の所は日本語化用のツールを置いているだけである。  
なおここのファイルを用いて起きた損害その他については一切の責任は利用者が負うものとする。

## 翻訳に関する注意事項
* **このゲームのセーブファイルはステージ名・武器名・インプラント名・臓器名・各資産（stocks）の短縮名などがそのまま含まれているテキストファイルなので、これらを日本語化するとオリジナルとはセーブデータの互換性が無くなる事に注意。**  
  また、これらの名称はプログラム内部でも識別子として使われているようなので、全ファイルで訳語を統一する必要もある。  
  ここを変更すると動作がオリジナルと変わってしまう可能性が発生し開発の方たちにご迷惑をおかけするかもしれないので、個人的には変更しない方がいいと思う。

## フォルダの説明
* bat  
  各種作業用バッチファイルの格納フォルダ。
  * 00_config.bat  
    作業対象のフォルダのパスなどを管理するバッチファイル。
  * 01_create_work_folder.bat  
    ワークフォルダを作成するバッチファイル。
  * 02_copy_unpacked_gd_files_to_work_dir.bat  
    *.gdファイルをワークフォルダにコピーして、バックアップフォルダを空にするバッチファイル。
  * 03_copy_unpacked_files_to_game_dir.bat  
    crueltysquad.pckをリネームし、アンパックしたファイル一式をゲームフォルダにコピーするバッチファイル。
  * 04_delete_unnecessary_files.bat  
    バックアップフォルダにワークフォルダから*.gdファイルを戻し、更に日本語化に不要なファイルを削除するバッチファイル。
  * 05_export_text.bat  
    ゲームファイルから英語テキストtsvファイルを抽出するスクリプト起動用バッチファイル。
  * 06_copy_japanese_font_file_to_game_dir.bat  
    日本語フォントファイルを入れ替え対象のフォントファイル名にリネームしてゲームのフォントフォルダにコピーするバッチファイル。
  * 07_import_text_and_copy_to_game_dir.bat  
    日本語テキストtsvファイルをアンパック・デコンパイルしたゲームファイルに埋め込んでゲームフォルダにコピーするスクリプト起動用バッチファイル。  
    埋め込みスクリプトが未修正のファイルに対してでないと正常動作しないため、スクリプト実行前に毎回バックアップフォルダのファイルをコピーして埋め込み対象にしている。  
    埋め込み処理が終わったらGodot Engineで*.gdcファイルをコンパイルした後、日本語を埋め込んだファイルをゲームフォルダにコピーする。
* py  
  Pythonスクリプトの格納フォルダ。
  * export_Cruelty-Squad_text.py  
    アンパック・デコンパイルしたゲームファイルから英語テキストtsvファイルを抽出するPythonスクリプトファイル。
  * import_Cruelty-Squad_text.py  
    日本語テキストtsvファイルをアンパック・デコンパイルしたゲームファイルに埋め込むPythonスクリプトファイル。


## ここのスクリプトで取り扱うテキストtsvファイルについて
抽出した英語テキストは引用符でくくらない、タブ文字（"\t"）区切りの文字列としてUTF-8で出力される。  
また全ての行の列数が同じではないので、行の終わりには"\t\[EOL\]"を付加して明確に分かるようにした。  
どの列に何のデータが入るかは対象ファイルの種類と文字別の種別によって異なる。  
抽出時のソートは2列目の昇順、1列目の昇順という順番で行われる。  
共通して改行はそのままでは使用不可なので、文字列内で改行したい場合は"\n"を書く。  
埋め込み時に空行は無視される。
* *.gd  
  デコンパイルしたGDScriptファイル。  
  このファイルの文字列には目印になるタグなどがないので、置換前文字列を置換後文字列で全置換する方法でテキスト埋め込みをする。  
  そのため「文字列が書かれていた行数」や「その行で何番目の文字列か」といった情報は埋め込み時に使わない。  
  これらは翻訳する際に参考にする情報である。  
  全置換するので同じ置換前文字列に違った置換後文字列を埋め込むこともできない。  
  こういう方法を取っているのはゲームがバージョンアップした際にも古い日本語ファイルの埋め込みができるようにするためである。
  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
  | --- | --- | --- | --- | --- | --- | --- |
  | 対象ファイルのルートからの相対パス | "gd" | 文字列が書かれていた行数 | その行で何番目の文字列か | 置換前文字列 | 置換後文字列 | "\[EOL\]" |
* *.json  
  JSONファイル。
  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | 対象ファイルのルートからの相対パス | "json" | "" | "" | キー"name"の文字列 | キー"objectives"の文字列 | キー"description"の文字列 | "\[EOL\]" |
* *.tscn  
  この種類のテキストファイルには複数の種別の文字別があるのでレイアウトもそれぞれ異なる。  
  基本的に\[node name="xxx" parent="yyy" index="z"\]といった形式のタグの直後に出現する「dialog_text = "文字列"」のような文字列を対象に抽出する。
  * DURATION  
    この種別は対象ファイルにおいて「DURATION = \[ 数値1, 数値2, ... , 数値x \]」といったリスト形式で書かれているため列数が可変である。  
    これはカットシーンでの字幕表示間隔で、DURATIONと同じタグの下に書かれているLINESがその時に表示する字幕のテキストである。  
    よってそのLINESと列数が同じになる。
    | 1 | 2 | 3 | 4 | 5 | 6 | 7 | ... | x + 5 | x + 6 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 対象ファイルのルートからの相対パス | "DURATION" | "" | "" | タグ | 数値1 | 数値2 | ... | 数値x | "\[EOL\]" |
  * DYN_LINES  
    この種別は対象ファイルにおいて「DYN_LINES = \[ \[ "文字列1" \],  \[ "文字列2", "文字列3" \], ... , \[ "文字列x-1", "文字列x-2", ... , "文字列x-y" \] \]」といった入れ子になったリスト形式で書かれているため列数が可変である。  
    抽出スクリプトの都合上、文字列内の改行は不可。  
    "\[SOB\]"は角括弧の開始、"\[EOB\]"は角括弧の終了を表している。
    | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | ... | ? | ? | ? | ... | ? | ? | ? |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 対象ファイルのルートからの相対パス | "DYN_LINES" | "" | "" | タグ | "\[SOB\]" | 文字列1 | "\[EOB\]" | "\[SOB\]" | 文字列2 | 文字列3 | "\[EOB\]" | ... | "\[SOB\]" | 文字列x-1 | 文字列x-2 | ... | 文字列x-y | "\[EOB\]" | "\[EOL\]" |
  * LINES  
    この種別は対象ファイルにおいて「LINES = \[ "文字列1", "文字列2", ... , "文字列x" \]」といったリスト形式で書かれているため列数が可変である。  
    文字列内で改行が入っている場合、"\n"に変換して出力する。
    | 1 | 2 | 3 | 4 | 5 | 6 | 7 | ... | x + 5 | x + 6 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 対象ファイルのルートからの相対パス | "LINES" | "" | "" | タグ | 文字列1 | 文字列2 | ... | 文字列x | "\[EOL\]" |
  * その他  
    以下の種別は全て同じレイアウトで出力される。  
    これらの項目はタグの下に存在しない場合、新たに追加される。  
    1. 文字列項目（値が「"」で括られている）
       * dialog_text
       * implant_name
       * level_name
       * line
       * line2
       * message
       * npc_name
       * override_name
       * text
       * value
    
    1. 非文字列項目（値が「"」で括られていない）  
       抽出処理では非文字列項目は対象にしていない。
       * margin_left
       * message
       * margin_right
       * margin_top
       * margin_bottom
       * custom_colors/font_color
      
    文字列内で改行が入っている場合、"\n"に変換して出力する。
    | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    | --- | --- | --- | --- | --- | --- | --- |
    | 対象ファイルのルートからの相対パス | 種別名 | "" | "" | タグ | 文字列 | "\[EOL\]" |

## 使い方
以下の説明に登場するフォルダなどのパスは下記を想定している。  
もし別のフォルダを使いたいならば  
*bat/00_config.bat*  
を修正すること。
* ゲームフォルダ  
  ゲームがインストールされているフォルダ  
  環境にもよるがゲームフォルダのパスはデフォルトだと下記になるはずである。    
  *"Steamインストールフォルダ/SteamApps/common/Cruelty Squad"*
* バックアップフォルダ  
  修正前のファイルを格納するフォルダ  
  *"C:\Temp/Cruelty Squad/pck_bak"*
* ワークフォルダ  
  修正後のファイルを格納するフォルダ  
  *"C:\Temp/Cruelty Squad/pck"*
* tsvフォルダ  
  テキストtsvファイルを格納するフォルダ  
  *"C:\Temp/Cruelty Squad/tsv"*  
  格納する各tsvファイル名は以下とする。
  * ゲームファイルから抽出した英語テキストtsvファイル  
    *"Cruelty-Squad_text_English.tsv"*  
  * 作成した日本語テキストtsvファイル  
    *"Cruelty-Squad_text_Japanese.tsv"*
* 日本語フォントフォルダ  
  日本語フォントの格納フォルダ。  
  *"C:\Temp/Cruelty Squad/japanese_font"*
* GodotEngine実行ファイル  
  *.gdファイルコンパイル用のGodot Engineの実行ファイル。  
  *"C:\Temp/Cruelty Squad/Godot_v3.5.2-stable_win64.exe/Godot_v3.5.2-stable_win64.exe"* 
* gdcプロジェクトフォルダ  
  *.gdファイルコンパイル用のGodotプロジェクトフォルダ。  
  *"C:\Temp/Cruelty Squad/gdc_project"* 
* gdcプロジェクトzipファイル  
  gdcプロジェクトをエクスポートしたzipファイル。  
  このzipファイルのパスをプロジェクトフォルダ内にしてしまうと次回エクスポートしたzipファイルがプロジェクトに組み込まれてしまうことには注意。  
  *"C:\Temp/Cruelty Squad/gdc_project.zip"* 
* gdcプロジェクトワークフォルダ  
  gdcプロジェクトzipファイルの解凍先フォルダ。  
  *"C:\Temp/Cruelty Squad/gdc_project_work"* 

例え日本語テキストtsvファイルを反映したいだけの場合も、一度は英語テキストtsvファイルを抽出する手順を実行しなければならない。  
但しその場合、05_export_text.batの実行だけは必要ない。
### 英語テキストtsvファイルを抽出するまで
1. まず以下をインストールする。
   * [Python](https://www.python.org/downloads/)  
     テキスト抽出・埋め込みスクリプト実行用。  
     バージョン3.11以上なら動くはず。
   * [Godot RE Tools](https://github.com/bruvzg/gdsdecomp/releases/)  
     crueltysquad.pckファイルのアンパックと*.gdファイルのデコンパイル用。
1. 下記のバッチファイルを実行して作業用フォルダを作成する。  
   *bat/01_create_work_folder.bat*
1. crueltysquad.pckをアンパック・デコンパイルする。
   1. Godot RE Toolsインストールフォルダのgdre_tools.exeを実行してメニューの"RE Tools"->"Recover project"を選ぶ。
   1. 開いたダイアログでCruelty Squadのゲームフォルダに格納されているcrueltysquad.pckを選択して"Open"を押す。  
   1. "Destination Folder"にバックアップフォルダを、"Options"に"Full Recovery"を選択して"Extract..."を押す。  
      この時に幾つかのファイルが変換できないというエラーが出た場合は無視していい。  
   1. 下記のバッチファイルを実行して*.gdファイルだけをワークフォルダにコピーして退避した後に、一旦バックアップフォルダを空にする。  
      *bat/02_copy_unpacked_gd_files_to_work_dir.bat*
   1. "Destination Folder"にバックアップフォルダを、"Options"に"Extract Only"を選択して"Extract..."を押す。  
1. Godot製のゲームは.pckファイルの代わりにアンパックしたファイル一式をそのまま同じフォルダに置くことでも動作させられるので、下記のバッチファイルを実行しcrueltysquad.pckをリネームしてバックアップを取った後に一式をコピーする。  
   *bat/03_copy_unpacked_files_to_game_dir.bat*
1. 下記のバッチファイルを実行してバックアップフォルダにワークフォルダから*.gdファイルを戻し、更に日本語化に不要なファイルを削除する。  
   *bat/04_delete_unnecessary_files.bat*
1. 下記のバッチファイルを実行してバックアップフォルダのゲームファイルから英語テキストtsvファイルを抽出する。  
   *bat/05_export_text.bat*  
   一度抽出してしまえば後はこのバッチを実行するだけで何回でも抽出しなおすことが出来る。

### 日本語テキストtsvファイルを反映するまで
1. まず以下をインストールする。
   * [Godot Engine 3.5.2](https://godotengine.org/download/3.x/windows)  
     *.gdファイルのコンパイル用。  
     GodotEngine実行ファイルのパスと一致するようにインストールする。
1. 日本語フォントフォルダに適当な日本語フォントを置いた後に下記のバッチファイルの"newFontFile"を書き換えて実行し、ゲームのフォントを入れ替える。  
   *bat/05_copy_japanese_font_file.bat*  
   私は日本語フォントに[ふぉんとうは怖い明朝体フリーフォント](http://www.fontna.com/%E3%81%B5%E3%81%89%E3%82%93%E3%81%A8%E3%81%86%E3%81%AF%E6%80%96%E3%81%84%E6%98%8E%E6%9C%9D%E4%BD%93/)を使わせて頂いた。  
   雰囲気だけで言えば[怨霊フォント 2.0](https://www.vector.co.jp/soft/win95/writing/se400162.html)の方が元のフォントに近いと思うのだが、ゲーム画面上だとあまりにも見づらかったので前者にした。
1. *.gdファイルコンパイル用のGodotプロジェクトを作成する。  
   1. Godot Engine 3.5.2インストールフォルダのGodot_v3.5.2-stable_win64.exeを実行して、プロジェクトマネージャーが表示されたら右端の"新規プロジェクト"を押す。  
      "プロジェクトが何も登録されていません。"のダイアログが表示された場合は"キャンセル"を押す。
   1. 開いたダイアログでプロジェクトパス"にgdcプロジェクトフォルダのパスを入力して"作成して編集"を押す。
   1. メニューの"プロジェクト"->"エクスポート..."を選ぶ。
   1. 開いた"エクスポート"ダイアログで"追加..."を押して"Windows Desktop"を選択する。
   1. 下にエラーメッセージが表示されるので、その中の"エクスポートテンプレートの管理"のリンクを押す。
   1. "ダウンロードしてインストール"を押し、ダウンロードが終わったら"閉じる"を押す。
   1. Godot Engineを閉じる。
1. 下記のバッチファイルを実行して日本語テキストtsvファイルをワークフォルダのゲームファイルに埋め込みGodot Engineで*.gdcファイルをコンパイルした後、日本語を埋め込んだファイルをゲームフォルダにコピーする。  
   *bat/07_import_text_and_copy_to_game_dir.bat*  
   一度埋め込みしてしまえば後はこのバッチを実行するだけで何回でも埋め込みなおすことが出来る。
   

# To Do
