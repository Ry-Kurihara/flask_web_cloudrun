## MyPortfolio 

### 概要
`https://flask-ut7dunfa5q-an.a.run.app/`に公開しています。

### Tools
- System
    - Flask
    - Flask-Migrate
    - Flask-Login
    - Google Cloud SQL
    - Google Cloud Run
- Designe
    - Bootstrap
    - AvantUi


### Tips
このアプリケーションで使用しているDBのスキーマ管理は[Migrationリポジトリ](https://github.com/Ry-Kurihara/flask_db_migration)で行なっています。

アプリケーションの実行にGCPサービスアカウントのキーを必要としています。ローカルで実行する場合はルートディレクトリにキーを`google.json`として保存し、以下のコマンドを実行してください。
```sh 
export GOOGLE_APPLICATION_CREDENTIALS="google.json"
```