## awsの資格の学習記録や対策などの管理を行う
資格試験の学習のためのリポジトリ

## 取得済み

<img width="1630" height="649" alt="aws-badges-20260509" src="https://github.com/user-attachments/assets/c1c76369-ad40-4251-ab80-9eec902d8a7b" />



## 未取得
- ANS

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
