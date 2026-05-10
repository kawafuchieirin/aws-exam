## Bedrock agent

##　帰属機能

## Converse API
Converse APIでは、Bedrockの基盤モデル対して共通したアクセスができるようになります。

InvokeModel APIのように、モデルごとの差異を意識することなく、モデルの切り替えが容易になります。

また、InvokeModel APIと同じようにStreamでの呼び出しも可能です。
このAPIを利用するためには、以下の権限が必要となります

bedrock:InvokeModel
bedrock:InvokeModelWithResponseStream。
ただし、現時点（2024/07/05）では、すべての基盤モデルで利用できるAPIではありませんので、ご注意ください。

https://dev.classmethod.jp/articles/amazon-bedrock-converse-api/

## top-k
op-k は、候補の中から スコアが高い順に上位 k 個だけを選ぶ という考え方です。
たとえば、検索結果や推薦システムで各候補にスコアが付いているとします。
候補スコアA0.92B0.85C0.73D0.40
このとき top-2 なら、上位2件の A と B を選びます。
よく使われる場面
検索・推薦
検索エンジンやベクトル検索で、問い合わせに最も近い文書を 上位 k 件 返すときに使います。
例：
top-k = 5
なら、関連度が高い順に5件だけ返します。
機械学習・分類
モデルが複数クラスの確率を出したとき、確率が高い上位 k クラスを見ることがあります。
例：
top-1 accuracy
は「一番確率が高い予測が正解か」を見る指標です。
top-5 accuracy
は「上位5個の予測の中に正解が含まれているか」を見る指標です。
生成AIの top-k サンプリング
文章生成では、次の単語候補のうち、確率が高い 上位 k 個 だけを残して、その中から選ぶ方法を指します。
例：
top-k = 50
なら、次に来る単語候補を確率上位50個に絞り、その中からサンプリングします。
まとめ
top-k = 上位 k 個を選ぶ処理です。


top-1 → 一番良いものだけ


top-5 → 上位5個


top-10 → 上位10個


検索、推薦、分類、生成AIなどでよく使われます。

## Amazon Comprehend
「Amazon Comprehend」は、AWSが提供している自然言語処理 (NLP) サービスで、機械学習を活用してテキストからインサイトを抽出できます。読み取ったテキストのキーフレーズの抽出や、感情の分析といった機能を備えており、日本語にも対応。拡張サービスとして、「Amazon Comprehend medical」という、医療文書の解析に特化したサービスもあります。

https://www.cloudsolution.tokai-com.co.jp/white-paper/2024/1213-532.html

## グラウンディングチェック
これにより、モデルレスポンスがソースに基づいて事実上正確であり、ソースに基づいているかどうかが確認されます。レスポンスに追加された新しい情報は、根拠がないと見なされます。
→AIの回答が事実に基づいているかを保証するためのもの
https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/guardrails-contextual-grounding-check.html
