# 🛠 Contributing Guidelines

안녕하세요! 이 프로젝트에 관심 가져주셔서 감사합니다. 원활하고 효율적인 협업을 위해 아래의 지침을 꼭 읽고 따라주시기 바랍니다.

---

## 📁 프로젝트 폴더 구조

```
C:.
│ .cache
│ .env
│ .gitignore
│ check.ipynb
│ check_pyreadline3.py
│ CONTRIBUTING.md
│ db.sqlite3
│ faq 크롤링.ipynb
│ faq.csv
│ faq_test.csv
│ manage.py
│ README.md
│ requirements.txt
│
├─.ipynb_checkpoints
│ faq 크롤링-checkpoint.ipynb
│ faq-checkpoint.csv
│
├─accounts
│ │ admin.py
│ │ apps.py
│ │ forms.py
│ │ models.py
│ │ signals.py
│ │ tests.py
│ │ urls.py
│ │ views.py
│ │ init.py
│ ├─migrations
│ ├─templates
│ └─pycache
│
├─bot
│ │ .gitignore
│ │ chatbot.py
│ │ mapping.py
│ │ responses.py
│ │ utils.py
│ └─pycache
│
├─chatbot
│ ├─management
│ ├─migrations
│ └─pycache
│
├─faq
│ │ admin.py
│ │ apps.py
│ │ forms.py
│ │ models.py
│ │ tests.py
│ │ urls.py
│ │ views.py
│ │ init.py
│ ├─management
│ ├─migrations
│ ├─templates
│ └─pycache
│
├─forum
│ │ admin.py
│ │ apps.py
│ │ forms.py
│ │ models.py
│ │ tests.py
│ │ urls.py
│ │ views.py
│ │ init.py
│ ├─migrations
│ ├─templates
│ └─pycache
│
├─home
│ │ admin.py
│ │ apps.py
│ │ bot_logic.py
│ │ consumers.py
│ │ dataset.csv
│ │ lastfm_utils.py
│ │ mapping.py
│ │ models.py
│ │ routing.py
│ │ tag_extractor.py
│ │ tests.py
│ │ urls.py
│ │ views.py
│ │ init.py
│ ├─migrations
│ ├─templates
│ └─pycache
│
├─images
│ 로고.png
│ 주제배경.png
│
├─locale
│ └─ko_KR
│ └─LC_MESSAGES
│ django.mo
│ django.po
│
├─media
│ └─avatars
│ default_avatar.png
│
├─music_project
│ │ asgi.py
│ │ settings.py
│ │ urls.py
│ │ wsgi.py
│ │ init.py
│ └─pycache
│
├─mypage
│ │ admin.py
│ │ apps.py
│ │ forms.py
│ │ models.py
│ │ tests.py
│ │ urls.py
│ │ views.py
│ │ init.py
│ ├─management
│ ├─migrations
│ ├─templates
│ └─pycache
│
├─scripts
│ create_missing_profiles.py
│ create_superuser.py
│
├─search
│ │ admin.py
│ │ apps.py
│ │ consumers.py
│ │ models.py
│ │ routing.py
│ │ tests.py
│ │ urls.py
│ │ views.py
│ │ init.py
│ ├─management
│ ├─migrations
│ ├─templates
│ └─pycache
│
├─static
│ └─images
│ moodyfy_logo.png
│
└─templates
│ base.html
│ index.html
│ music_player_popup.html
└─socialaccount
login.html
```

---

## ✅ 커밋 메시지 규칙

- 커밋 메시지는 작업의 **의도와 변경사항**을 명확히 전달해야 합니다.
- 아래의 prefix를 사용하여 커밋 유형을 명시해주세요.

| 타입 | 설명 |
|------|------|
| `feat:` | 새로운 기능 추가 |
| `fix:` | 버그 수정 |
| `refactor:` | 코드 리팩토링 (기능 변화 없음) |
| `docs:` | 문서 작성/수정 |
| `style:` | 코드 포맷팅 (세미콜론, 들여쓰기 등 비기능 수정) |

**예시:**
```bash
feat: [홍길동] 데이터셋 csv load 기능 추가
fix: [김지민] 전처리 오류 수정
docs: [우지훈] README에 프로젝트 목적 추가
```

---

## 📦 라이브러리 및 의존성 관리

1. **새로운 라이브러리 설치 시:**
```bash
pip install <package-name>
```

2. **설치한 라이브러리를 `requirements.txt`에 반영:**
```bash
pip freeze > requirements.txt
```

3. **다른 팀원이 환경을 맞추는 방법:**
```bash
pip install -r requirements.txt
```

> ⚠️ 가상환경 사용을 권장합니다:  
> `python -m venv venv` → `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)

---

## 🧼 코드 컨벤션

- **Python 버전**: 3.9 이상 권장
- **형식 통일을 위해** `black`, `flake8`, `isort` 등의 사용을 권장합니다.
- PR(Pull Request) 전에는 반드시 코드를 정리하고 커밋해주세요.

---

필요 시 이 문서는 언제든지 업데이트될 수 있습니다. 변경 사항은 PR 또는 팀 회의 등을 통해 공유해주세요.  
좋은 협업을 기대합니다 😊
