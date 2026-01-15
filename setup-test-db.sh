#!/bin/bash
set -e

# テスト用DB設定
DB_NAME="mine2_test"
DB_USER="pdbj"
DB_PORT="5433"
SOURCE_DB="mine2"
SAMPLE_COUNT=100  # テスト用エントリー数

echo "=== テスト用DB (${DB_NAME}) セットアップ ==="

# 1. 既存のテストDBがあれば削除
echo "1. 既存のテストDBを削除..."
psql -U $(whoami) postgres -p $DB_PORT -c "DROP DATABASE IF EXISTS ${DB_NAME};" 2>/dev/null || true

# 2. テストDBを作成
echo "2. テストDBを作成..."
psql -U $(whoami) postgres -p $DB_PORT -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

# 3. 本番DBからスキーマのみをダンプして適用
echo "3. スキーマをコピー..."
pg_dump -U $DB_USER -p $DB_PORT -s $SOURCE_DB 2>/dev/null | psql -U $DB_USER -p $DB_PORT -d $DB_NAME -q 2>/dev/null

# 4. brief_summaryからランダムにサンプルを選択してPDBIDリストを作成
echo "4. サンプルデータを選択（${SAMPLE_COUNT}件）..."
PDBIDS=$(psql -U $DB_USER -p $DB_PORT -d $SOURCE_DB -t -A -c \
    "SELECT pdbid FROM pdbj.brief_summary ORDER BY random() LIMIT ${SAMPLE_COUNT};")

# PDBIDをカンマ区切りの文字列に変換（SQLで使う形式）
PDBID_LIST=$(echo "$PDBIDS" | tr '\n' ',' | sed 's/,$//' | sed "s/\([^,]*\)/'\1'/g")

echo "5. 外部キー制約を一時無効化..."
# 全ての外部キー制約を取得して無効化
psql -U $DB_USER -p $DB_PORT -d $DB_NAME -t -A -c \
    "SELECT 'ALTER TABLE \"' || nspname || '\".\"' || relname || '\" DROP CONSTRAINT IF EXISTS \"' || conname || '\";'
     FROM pg_constraint c
     JOIN pg_class cl ON c.conrelid = cl.oid
     JOIN pg_namespace n ON cl.relnamespace = n.oid
     WHERE c.contype = 'f' AND n.nspname = 'pdbj';" | \
    psql -U $DB_USER -p $DB_PORT -d $DB_NAME -q 2>/dev/null || true

echo "6. サンプルデータを投入..."

# 全テーブルを取得（pdbj スキーマ内）- 元の名前を保持
TABLES=$(psql -U $DB_USER -p $DB_PORT -d $SOURCE_DB -t -A -c \
    "SELECT tablename FROM pg_tables WHERE schemaname = 'pdbj';")

# 各テーブルからpdbidに該当するデータをコピー
for table in $TABLES; do
    # テーブルにpdbidカラムがあるか確認（テーブル名をダブルクォート）
    HAS_PDBID=$(psql -U $DB_USER -p $DB_PORT -d $SOURCE_DB -t -A -c \
        "SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='pdbj' AND table_name='${table}' AND column_name='pdbid');")
    
    if [ "$HAS_PDBID" = "t" ]; then
        # pdbidでフィルタリングしてデータをコピー（テーブル名をダブルクォート）
        COUNT=$(psql -U $DB_USER -p $DB_PORT -d $SOURCE_DB -t -A -c \
            "SELECT COUNT(*) FROM pdbj.\"${table}\" WHERE pdbid IN (${PDBID_LIST});")
        if [ "$COUNT" -gt 0 ]; then
            echo "  - ${table} (${COUNT}件)..."
            psql -U $DB_USER -p $DB_PORT -d $SOURCE_DB -c \
                "COPY (SELECT * FROM pdbj.\"${table}\" WHERE pdbid IN (${PDBID_LIST})) TO STDOUT" 2>/dev/null | \
            psql -U $DB_USER -p $DB_PORT -d $DB_NAME -c "COPY pdbj.\"${table}\" FROM STDIN" 2>/dev/null
        fi
    fi
done

echo ""
echo "7. 外部キー制約を再作成（スキーマから復元）..."
pg_dump -U $DB_USER -p $DB_PORT -s $SOURCE_DB 2>/dev/null | grep -E "^ALTER TABLE.*ADD CONSTRAINT.*FOREIGN KEY" | \
    psql -U $DB_USER -p $DB_PORT -d $DB_NAME -q 2>/dev/null || true

# 8. 投入結果の確認
echo ""
echo "=== 投入結果 ==="
psql -U $DB_USER -p $DB_PORT -d $DB_NAME -c "SELECT COUNT(*) as entries FROM pdbj.brief_summary;"

# 主要テーブルの件数
echo ""
echo "=== 主要テーブルの件数 ==="
psql -U $DB_USER -p $DB_PORT -d $DB_NAME -c "
SELECT 'entry' as table_name, COUNT(*) as count FROM pdbj.entry
UNION ALL SELECT 'entity', COUNT(*) FROM pdbj.entity
UNION ALL SELECT 'struct', COUNT(*) FROM pdbj.struct
UNION ALL SELECT 'exptl', COUNT(*) FROM pdbj.exptl
ORDER BY table_name;"

echo ""
echo "=== セットアップ完了 ==="
echo "テスト用DBに接続: psql -U ${DB_USER} -p ${DB_PORT} -d ${DB_NAME}"
echo ""
echo "worktree側で使用する場合は config.test.yml を参照してください"
