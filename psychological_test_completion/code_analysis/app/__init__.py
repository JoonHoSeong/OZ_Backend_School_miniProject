import os
import click
from datetime import datetime, timedelta
from flask import Flask
from flask_migrate import Migrate
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from .database import db
from .models import Question, Admin, Participant  # Question 모델 임포트

def create_app():
    app = Flask(__name__)
    app.secret_key = "oz_coding_secret"

    # 데이터베이스 파일 경로 설정 및 앱 설정
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dbfile = os.path.join(basedir, "db.sqlite")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbfile
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 데이터베이스 및 마이그레이션 초기화
    db.init_app(app)
    migrate = Migrate(app, db)

    # 라우트(블루프린트) 등록
    from .routes import main as main_blueprint
    from .routes import admin as admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)

    # 초기화 명령어 정의
    def add_initial_questions():
        ## 질문 리스트 초기화
        initial_questions = [
            "오즈코딩스쿨에 대해서 알고 계신가요?",
            "프론트엔드 과정에 참여하고 계신가요?",
            "전공자 이신가요?",
            "프로젝트를 진행해보신적 있으신가요?",
            "개발자로 일한 경력이 있으신가요?",
        ]
        ## 어제 날자 계산시 utfnow -> now로 변경
        yesterday = datetime.now() - timedelta(days=1)  # 어제 날짜 계산

        # 관리자 계정 추가 로직, 비밀번호 해시 처리 적용
        existing_admin = Admin.query.filter_by(username="admin").first()
        # 관리자 계저이 없을시 계정 및 비밀번호 추가
        if not existing_admin:
            hashed_password = generate_password_hash("0000")  # 비밀번호를 해시 처리
            new_admin = Admin(username="admin", password=hashed_password)
            db.session.add(new_admin)

        # 참여자의 참여일시가 없는 데이터들은 어제 일자로 참여 일시를 변경
        participants_without_created_at = Participant.query.filter(
            Participant.created_at == None
        ).all()

        for participant in participants_without_created_at:
            participant.created_at = yesterday

        # 저장된 질문과 초기 질문이 다를시 질문 리스트 데이터 베이스에 추가
        for question_content in initial_questions:
            existing_question = Question.query.filter_by(
                content=question_content
            ).first()
            
            if not existing_question:
                new_question = Question(content=question_content)
                db.session.add(new_question)
        questions = Question.query.all()
        for question in questions:
            question.order_num = question.id
            question.is_active = True  # 모든 질문을 활성화 상태로 설정
        db.session.commit()
        
    #flask init-db 실행시 DB에 테이블 들을 세팅해줌 
    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        db.create_all()
        add_initial_questions()
        click.echo("Initialized the database.")

    app.cli.add_command(init_db_command)

    return app
