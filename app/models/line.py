from app import db

class LineBaseMessages(db.Model):
    __tablename__ = 'line_base_message'
    __table_args__ = {'extend_existing': True}
    base_msg = db.Column(db.Text, unique=True, primary_key=True)
    reply_msg = db.Column(db.Text)

    def __init__(self, base_msg=None, reply_message=None):
        self.base_msg = base_msg 
        self.reply_message = reply_message

class MessageHistory(db.Model):
    __tablename__ = 'line_message_history'
    __table_args__ = {'extend_existing': True}
    message = db.Column(db.Text, primary_key=True)
    timestamp = db.Column(db.Text, primary_key=True)
    user_id = db.Column(db.Text, primary_key=True)

    def __init__(self, message=None, timestamp=None, user_id=None):
        self.message = message
        self.timestamp = timestamp
        self.user_id = user_id

    def __repr__(self):
        return '<Message_History message:{} user_id:{} timestamp:{}>'.format(self.message, self.user_id, self.timestamp)