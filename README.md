## awsの資格の学習記録や対策などの管理を行う

## 取得済み
資格試験の学習のためのリポジトリ
<img width="1496" height="670" alt="aws-badges-20260412" src="https://github.com/user-attachments/assets/acfbbe46-690a-45d5-9213-b18ee2e7e3e3" />



## 未取得
- ANS
- SCS
- AIP


## ディレクトリ構成

```text
.
├── README.md
└── badge-generator/
    ├── index.html
    ├── badge-data.js
    └── images/
        ├── AIF.png
        ├── ANS.png
        ├── CLF.png
        ├── DEA.png
        ├── DOP.png
        ├── DVA.png
        ├── MLA.png
        ├── SAA.png
        ├── SAP.png
        ├── SCS.png
        └── SOA.png
```

## badge-generatorの使い方

AWS認定バッジの一覧画像を生成するためのツールです。

```bash
cd badge-generator
python3 -m http.server 8000
```

ブラウザで以下にアクセスします。

```text
http://localhost:8000
```

取得済みの資格を「クリア」に変更し、「バッジ画像を生成」を押すと画像を生成できます。
