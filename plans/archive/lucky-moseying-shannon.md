# mine2updater-ng プロジェクト調査結果

## 概要

mine2updater-ngは、PDBj（Protein Data Bank Japan）が提供するオリジナルのmine2updaterをTypeScriptでリファクタリングしたプロジェクト。構造生物学データをrsyncで同期し、PostgreSQLデータベースにロードするCLIツール。

## 技術スタック

| 項目 | 技術 |
|------|------|
| メイン言語 | TypeScript (ES2022, strict mode) |
| ランタイム | Node.js 18.12.1+ |
| データベース | PostgreSQL 12+ (libpq native) |
| 補助スクリプト | Python 3.10+ (gemmi, CIF変換) |
| 環境管理 | Pixi (Conda互換) |
| CLI | Commander.js |

## コード規模

- **総行数**: 約7,000行 (TypeScript)
- **ソースファイル**: 20ファイル
- **ライセンス**: GNU LGPLv3

## ディレクトリ構造

```
mine2updater-ng/
├── src/
│   ├── mine2.ts           # CLIエントリーポイント (167行)
│   ├── commands/          # コマンド実装 (644行)
│   │   ├── sync.ts        # rsync同期
│   │   ├── update.ts      # パイプライン実行
│   │   └── test.ts        # テスト用DB作成・検証
│   ├── modules/           # コアモジュール (3,527行)
│   │   ├── rdb-helper.ts  # PostgreSQLヘルパー (1,215行) [最大]
│   │   ├── rdb-loader.ts  # データローダー (796行)
│   │   ├── cif.ts         # CIF/mmJSONパーサー (686行)
│   │   ├── general.ts     # ユーティリティ (518行)
│   │   ├── pg-native-custom.ts # libpqラッパー (503行)
│   │   └── rdb-worker.ts  # ワーカープロセス (309行)
│   ├── pipelines/         # データパイプライン (1,922行)
│   │   ├── pdbj.load.ts   # PDB構造データ (582行)
│   │   ├── ihm.load.ts    # 統合ハイブリッドモデル (535行)
│   │   ├── vrpt.load.ts   # バリデーションレポート (248行)
│   │   ├── cc.load.ts     # 化学成分辞書 (146行)
│   │   ├── prd.load.ts    # BIRDデータ (122行)
│   │   ├── ccmodel.load.ts # 化学成分モデル (109行)
│   │   ├── emdb.load.ts   # 電子顕微鏡DB (94行)
│   │   └── contacts.load.ts # タンパク質コンタクト (85行)
│   └── types/             # 型定義 (237行)
├── scripts/
│   ├── patch-libpq.js     # libpqパッチ
│   └── cif2json.py        # CIF→JSON変換ユーティリティ
├── config.yml             # 本番設定
├── config.test.yml        # テスト設定
├── package.json
├── pixi.toml
└── tsconfig.json
```

## 主要コマンド

| コマンド | 説明 |
|----------|------|
| `sync [targets...]` | PDBjからrsyncでデータ同期 (pdbj, cc, ccmodel, prd, vrpt, contacts, schemas, dictionaries) |
| `update [pipelines...]` | DBパイプライン実行 (pdbj, cc, ccmodel, prd, vrpt, contacts) |
| `all` | sync + update の一括実行 |
| `test` | テストDB作成・パイプライン検証 |
| `convert-vrpt` | CIF→JSON変換ユーティリティ |

## アーキテクチャ特徴

1. **クラスタベース並列処理**: Node.js clusterで最大16ワーカー
2. **スキーマ駆動**: YAML定義からDBスキーマを自動生成
3. **差分計算**: 変更分のみを更新（delta calculation）
4. **パイプライン設計**: 各データタイプに独立したローダー
5. **Native PostgreSQL**: libpqによる高速DB接続

## データフロー

```
PDBj servers
    ↓ (rsync)
Local data files (mmJSON/CIF)
    ↓ (pipelines)
PostgreSQL Database
```

## 現状の課題・改善候補

1. **テスト**: ユニットテストフレームワーク未導入（現在はE2Eのみ）
2. **CI/CD**: GitHub Actions等の設定なし
3. **リンター**: ESLint/Prettier未設定（TypeScript）
4. **ドキュメント**: 内部APIドキュメントなし

---

**調査完了**: プロジェクト全体の構造と機能を把握しました。
