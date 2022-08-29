# -*- coding: utf-8 -*-
from app import create_app
app = create_app()

from app.my_lib import log_config
logger = log_config.setup_logger('app.flask')

# Flask-Migrate
from flask_migrate import Migrate 
from app import db 
migrate = Migrate(app, db)

if __name__ == "__main__":
    # flask付属のWSGIサーバーで起動させる場合（python flask_app.py）はこちらのコマンドを実行している。gunicornコマンドを使用した際はapp.runは実行されていない。
    app.run(debug=True, host="0.0.0.0", port=8000)