import os
import uuid
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import easyocr
from googletrans import Translator
from dotenv import load_dotenv

app = Flask(__name__)

# 환경변수
load_dotenv() 

# 업로드 경로 설정 (절대경로)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# DB 연결 정보
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'cursorclass': pymysql.cursors.DictCursor
}

app.secret_key = os.getenv('SECRET_KEY')  # 세션용 비밀키


# ------------------ 회원가입 ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pw_hash = generate_password_hash(password)

        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 중복 이메일 체크
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        exist = cursor.fetchone()
        if exist:
            conn.close()
            return "이미 존재하는 이메일입니다."

        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
            (email, pw_hash)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')


# ------------------ 로그인 ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['email'] = email
            return redirect(url_for('dashboard_home'))
        else:
            return "이메일 또는 비밀번호가 잘못되었습니다."

    return render_template('login.html')


# ------------------ 로그아웃 ------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ------------------ 홈 화면 ------------------
@app.route('/')
def home():
    # 로그인 상태면 로그인 전용 홈(dashboard_home.html)로 이동
    if 'user_id' in session:
        return render_template('dashboard_home.html', title='내 홈', header_title='내 홈')
    # 비로그인 상태면 기존 소개 페이지
    return render_template('home.html', title='OCR 시스템 홈', header_title='홈')


# ------------------ 대시보드 화면 ------------------
@app.route('/dashboard_home')
def dashboard_home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard_home.html', title='대시보드 홈', header_title='대시보드 홈')


# ------------------ 컬렉션 목록 ------------------
@app.route('/collections')
def list_collections():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, created_at
        FROM collections
        WHERE user_id=%s
        ORDER BY created_at DESC
    """, (session['user_id'],))
    collections = cursor.fetchall()
    conn.close()

    return render_template('collections.html', collections=collections)


# ------------------ 컬렉션 추가 ------------------
@app.route('/collections/add', methods=['GET', 'POST'])
def add_collection():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        desc = request.form.get('description', '')

        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO collections (user_id, name, description)
            VALUES (%s, %s, %s)
        """, (session['user_id'], name, desc))
        conn.commit()
        conn.close()

        return redirect(url_for('list_collections'))

    return render_template('add_collection.html')


# ------------------ 업로드 페이지 (GET) ------------------
@app.route('/upload', methods=['GET'])
def upload_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 현재 유저의 컬렉션 목록을 가져와서 드롭다운에 표시
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM collections WHERE user_id=%s", (session['user_id'],))
    collections = cursor.fetchall()
    conn.close()

    return render_template(
        'upload.html',
        title='이미지 업로드',
        header_title='이미지 업로드',
        collections=collections
    )


# ------------------ 파일 업로드 (POST) ------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    file = request.files.get('image')
    if not file:
        return jsonify({'error': '파일이 없습니다.'}), 400

    original_lang = 'ko'
    target_lang = request.form.get('target_lang', 'en')
    collection_id = request.form.get('collection_id')  # 문자열로 들어옴

    # 파일 이름 재생성 (UUID)
    ext = os.path.splitext(file.filename)[1]  # .png, .jpg 등
    filename = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    db_path = f"/static/uploads/{filename}"

    file.save(save_path)

    # DB 저장
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO images (user_id, collection_id, image_path, original_lang, target_lang, status)
        VALUES (%s, %s, %s, %s, %s, 'UPLOADED')
    """, (user_id, collection_id, db_path, original_lang, target_lang))
    conn.commit()
    conn.close()

    print(f"✅ 업로드 완료: user_id={user_id}, file={filename}, collection_id={collection_id}")
    return redirect(url_for('list_images', collection_id=collection_id if collection_id else None))


# ------------------ OCR 실행 ------------------
@app.route('/ocr/<int:image_id>', methods=['GET'])
def run_ocr(image_id):
    if 'user_id' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    try:
        # 1️⃣ DB에서 이미지 경로 조회
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT image_path
            FROM images
            WHERE id=%s AND user_id=%s
        """, (image_id, session['user_id']))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({'error': '해당 ID의 이미지가 없습니다.'}), 404

        image_path = result['image_path']  # /static/uploads/abc.png
        abs_path = os.path.join(app.root_path, image_path.lstrip('/'))

        if not os.path.exists(abs_path):
            return jsonify({'error': f'파일을 찾을 수 없습니다: {abs_path}'}), 404

        # 2️⃣ OCR 실행
        reader = easyocr.Reader(['ko', 'en'], gpu=False)
        ocr_result = reader.readtext(abs_path, detail=0)
        extracted_text = "\n".join(ocr_result)

        print(f"✅ OCR 텍스트 추출 완료: {len(extracted_text)}자")

        # 3️⃣ DB 업데이트
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE images
            SET ocr_text=%s, status='OCR_DONE', updated_at=NOW()
            WHERE id=%s AND user_id=%s
        """, (extracted_text, image_id, session['user_id']))
        conn.commit()
        affected = cursor.rowcount
        conn.close()

        print(f"✅ DB 업데이트 완료 (rows={affected})")

        return jsonify({
            'message': 'OCR 완료!',
            'image_id': image_id,
            'extracted_text': extracted_text
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ------------------ 번역 실행 ------------------
@app.route('/translate/<int:image_id>', methods=['GET'])
def translate_text(image_id):
    if 'user_id' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1️⃣ OCR 텍스트 가져오기
        cursor.execute("""
            SELECT ocr_text, target_lang
            FROM images
            WHERE id=%s AND user_id=%s
        """, (image_id, session['user_id']))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return jsonify({'error': '해당 ID의 이미지가 없습니다.'}), 404

        ocr_text = result['ocr_text']
        target_lang = result['target_lang']

        if not ocr_text:
            conn.close()
            return jsonify({'error': 'OCR 결과가 없습니다. 먼저 OCR을 실행하세요.'}), 400

        # 2️⃣ Googletrans 번역 수행
        translator = Translator()
        translated = translator.translate(ocr_text, dest=target_lang)
        translated_text = translated.text

        # 3️⃣ 번역 결과 DB 저장
        cursor.execute("""
            UPDATE images
            SET translated_text=%s, status='TRANSLATED'
            WHERE id=%s AND user_id=%s
        """, (translated_text, image_id, session['user_id']))
        conn.commit()
        conn.close()

        return jsonify({
            'message': '번역 완료!',
            'image_id': image_id,
            'translated_text': translated_text
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ------------------ 이미지 리스트 ------------------
@app.route('/list')
def list_images():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    collection_id = request.args.get('collection_id')

    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = """
        SELECT id, collection_id, image_path, ocr_text, translated_text, status, created_at
        FROM images
        WHERE user_id = %s
    """
    params = [user_id]

    if collection_id:
        sql += " AND collection_id = %s"
        params.append(collection_id)

    sql += " ORDER BY created_at DESC"

    cursor.execute(sql, params)
    images = cursor.fetchall()
    conn.close()

    return render_template('list.html', images=images, current_collection_id=collection_id)


# ------------------ OCR 텍스트 직접 수정 ------------------
@app.route('/update_ocr/<int:image_id>', methods=['POST'])
def update_ocr(image_id):
    if 'user_id' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    new_text = request.json.get('ocr_text')
    if not new_text:
        return jsonify({'error': '수정할 내용이 없습니다.'}), 400

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE images
            SET ocr_text=%s, status='OCR_DONE'
            WHERE id=%s AND user_id=%s
        """, (new_text, image_id, session['user_id']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'OCR 텍스트가 수정되었습니다.', 'ocr_text': new_text})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ------------------ 이미지 삭제 ------------------
@app.route('/delete/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    if 'user_id' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 이미지 경로 확인
        cursor.execute("""
            SELECT image_path
            FROM images
            WHERE id=%s AND user_id=%s
        """, (image_id, session['user_id']))
        img = cursor.fetchone()
        if not img:
            conn.close()
            return jsonify({'error': '해당 이미지를 찾을 수 없습니다.'}), 404

        image_path = img['image_path']

        # DB에서 삭제
        cursor.execute("DELETE FROM images WHERE id=%s AND user_id=%s", (image_id, session['user_id']))
        conn.commit()
        conn.close()

        # 실제 파일 삭제
        abs_path = os.path.join(os.getcwd(), image_path.lstrip('/'))
        if os.path.exists(abs_path):
            os.remove(abs_path)

        return jsonify({'message': '이미지가 삭제되었습니다.', 'image_id': image_id})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
