import bcrypt

# パスワードのハッシュ化
def get_password_hash(password: str):
    # bcrypt.hashpw()でパスワードをハッシュ化, bcrypt.gensalt()でソルトを生成
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12, prefix=b'2b')).decode('utf-8')

# パスワードの検証
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))