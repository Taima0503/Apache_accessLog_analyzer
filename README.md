## Name
Apache_accessLog_analyzer  
  
  
## Overview
this application visualize the number of access per hour and count the access of same user.  
Apache HTTP サーバへのアクセスログから、時間ごとのアクセス数と同じユーザーからのアクセス総数を出力します。  
  
  
## Description
Apache HTTP サーバへのアクセスログを分析するプログラムで5つの特徴を持っています。  

1.メモリを超えるようなアクセスログを扱える。  
　1万のダミーアクセスログを用いてメモリ使用量を計測したところ  
　     実行前(min)　69MB ->　実行時(max)　91MB  
程度のメモリ量で抑えられています。大規模なアクセスログの分析にも実行が可能です。  
  
2.同じディレクトリ内にあるアクセスログを包括的に分析できる。  
　pythonの正規化ライブラリ｢re｣を用いることで、検索語句と部分一致するようなファイル名をまとめて読みことができるようなっています。また、コマンドラインで部分一致での検索か完全一致の検索か設定できるため分析のニーズに幅広く対応しております。  
  
3.時間ごとのアクセス数はグラフによる可視化出力、ユーザーのアクセス総数にはcsvファイル出力をする。  
　分析の結果をすぐに考察できるよう出力はグラフによって可視化しています。さらに、ユーザーのアクセス総数は集計後、管理しやすいようcsvファイルによって出力されます。  
   
4.オプション機能による期間を絞った検索  
　コマンドライン上で実行する際、オプションで期間を指定できるようにしました。期間内のアクセスログのみ集計します。  
   
5.一部欠損したアクセスログにも停止することなく実行できる。  
　欠損データに対しては処理を飛ばすことで煩わしい修正作業などせず分析を進めることができます。  
   
   
##Requirement  
Python 3.6.5  
  packages-> 
  re,  
  csv,  
  glob,  
  argparse,  
  datetime,  
  collections,  
  matplotlib.pyplot  
               
               
##Usage  
windows10上での利用法を示します。  
  
Step.1 Requirementの環境を整え、"Apache_analysis.py"をダウンロードします。  
Step.2 コマンドプロンプトを起動し下のように記述し実行します。  
C:> python Apache_analysis.py 検索ファイル名※必須 --s_term 年/月/日※任意 --e_term 年/月/日※任意 --output_name 出力ファイル名※任意  
  
このとき、検索ファイル名に例のように｢*｣を付け加えることで部分一致検索となります。  
ex) python Apache_analysis.py access* --s_term 2005/4/18 --e_term 2005/4/18 --output_name result  
→｢access～｣となるようなファイル名すべてに対して分析を実行できます。出力ファイル名はcsvファイルの名前です。デフォルトは｢result(現在時刻).csv｣です。上書きをするかなど状況によって指定してください。

