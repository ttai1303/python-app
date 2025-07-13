import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db() :
    conn = sqlite3.connect('data/database.db')
    conn.row_factory = dict_factory
    return conn

def create_user(name,email,password) :
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name,email, password))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_email(email) :
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password, gender, avatar, telephone, birthday FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_email_and_password(email, password) :
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password, gender, avatar, telephone, birthday FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_avatar(user_id, avatar):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('UPDATE users SET avatar = ? WHERE id = ?',(avatar, user_id))
    conn.commit()
    conn.close()

def update_user_in_db(user_id, name, gender, email, telephone, birthday):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute("UPDATE users SET name = ?, gender = ?, email = ?, telephone = ?, birthday = ? WHERE id = ?", (name, gender, email, telephone, birthday, user_id))
    conn.commit()
    conn.close()

def get_all_videos():
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('SELECT * FROM video')
    videos = cursor.fetchall()
    conn.close()
    return videos

def get_video_by_id(video_id):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('SELECT * FROM video WHERE id = ?', (video_id,))
    video = cursor.fetchone()
    conn.close()
    return video

def get_video_by_name(name):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute('SELECT * FROM video WHERE title LIKE ?', (f'%{name}%',))
    videos = cursor.fetchall()
    conn.close()
    return videos

def add_to_favorites(user_id, video_id):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO favorite(user_id, video_id) VALUES (?, ?)', (user_id, video_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def remove_from_favorites(user_id, video_id):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM favorite WHERE user_id = ? AND video_id = ?', (user_id, video_id))
    conn.commit()
    conn.close()

def get_user_favorites(user_id):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    
    # First get all favorite video_ids for this user
    cursor.execute('SELECT video_id FROM favorite WHERE user_id = ?', (user_id,))
    favorite_video_ids = [row['video_id'] for row in cursor.fetchall()]
    
    # Then get all videos and filter
    cursor.execute('SELECT * FROM video')
    all_videos = cursor.fetchall()
    conn.close()
    
    # Filter videos that are in favorite_video_ids
    return [video for video in all_videos if video['id'] in favorite_video_ids]

def is_favorite(user_id, video_id):
    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM favorite WHERE user_id = ? AND video_id = ?', (user_id, video_id))
    result = cursor.fetchone() is not None
    conn.close()
    return result