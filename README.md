# 📘 Book OCR & Translation Platform  
AI 기반 OCR + 자동 번역 + Docker CI/CD 클라우드 배포 시스템  

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey)
![Gunicorn](https://img.shields.io/badge/WSGI-Gunicorn-brightgreen)
![EasyOCR](https://img.shields.io/badge/EasyOCR-Text%20Recognition-orange)
![Googletrans](https://img.shields.io/badge/Googletrans-Auto%20Translation-green)
![MySQL](https://img.shields.io/badge/Database-MySQL-blue)
![Nginx](https://img.shields.io/badge/Proxy-Nginx-green)
![Docker](https://img.shields.io/badge/Container-Docker-informational)
![GitHubActions](https://img.shields.io/badge/CI/CD-GitHub_Actions-lightblue)
![SSL](https://img.shields.io/badge/Security-HTTPS%20%2F%20Certbot-yellow)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 📖 목차
1. [프로젝트 개요](#-프로젝트-개요)
2. [아키텍처 개요](#-아키텍처-개요)
3. [핵심 기능](#-핵심-기능)
4. [기술 스택](#-기술-스택)
5. [디렉토리 구조](#-디렉토리-구조)
6. [환경 구성](#-환경-구성)
7. [CI/CD 파이프라인](#-cicd-파이프라인)
8. [보안 및 인증서 구성](#-보안-및-인증서-구성)
9. [향후 계획 (클라우드 확장)](#-향후-계획)
10. [개발자](#-개발자)

---

## 📖 프로젝트 개요
**Book OCR & Translation Platform**은  
AI 기반 **OCR(EasyOCR)** 기술로 텍스트를 추출하고,  
**Googletrans**로 영어 번역을 수행하는  
**Flask + Gunicorn + Nginx** 기반 클라우드 플랫폼입니다.

> 🎯 **개발 목적**
> - Gunicorn을 통한 안정적인 Flask 프로덕션 배포  
> - 클라우드 환경에서 확장 가능한 MSA 구조 설계  
> - CI/CD 자동 배포 포함한 실무형 DevOps 아키텍처 구축

---

## ☁️ 아키텍처 개요

```bash
Client ──► HTTPS(443)
            │
            ▼
       [ Nginx (Reverse Proxy + Load Balancer) ]
            │
            ▼
       [ Gunicorn (WSGI Server) ]
            │
            ▼
       [ Flask (OCR & Translation Logic) ]
            │
            ▼
       [ MySQL Database ]
```

| 구성요소 | 설명 |
|-----------|------|
| **Flask (App)** | OCR/번역/DB 처리 담당, Gunicorn으로 실행 |
| **Gunicorn** | Flask 앱을 WSGI 방식으로 멀티 워커로 운영 |
| **Nginx** | 리버스 프록시 + HTTPS 인증서 관리 + 로드밸런싱 |
| **Docker Compose** | 멀티컨테이너 앱 통합 실행 |
| **GitHub Actions** | 빌드 → 테스트 → Docker Hub 푸시 자동화 (CI) |
| **deploy_update.sh** | 서버 자동 배포 스크립트 (CD 트리거) |
| **Certbot** | SSL 인증서 자동 갱신 (HTTPS 보안 통신) |

---

## 🚀 핵심 기능

| 기능 | 설명 |
|------|------|
| 🧠 **OCR 인식** | EasyOCR로 이미지 내 텍스트 자동 추출 |
| 🌐 **자동 번역** | Googletrans API로 영어 번역 수행 |
| 📤 **이미지 업로드** | 업로드 및 미리보기 |
| 📚 **컬렉션 관리** | 책 단위로 OCR 이미지 그룹화 |
| ✏️ **OCR 결과 수정** | 추출된 텍스트를 직접 수정 및 재저장 |
| 💾 **MySQL 연동** | OCR, 번역 결과를 DB에 저장 |
| 🔒 **사용자 인증** | 회원가입 / 로그인 / 세션 유지 |
| ☁️ **로드밸런싱** | Nginx → Gunicorn → Flask 앱 서버 3개로 트래픽 분산 |
| ⚙️ **CI/CD 자동화** | GitHub push → Docker Hub → 서버 자동배포 |

---

## 🧩 기술 스택

| 구분 | 기술 |
|------|------|
| **Language / Framework** | Python 3.10 / Flask |
| **WSGI Server** | Gunicorn |
| **OCR & Translation** | EasyOCR, Googletrans |
| **Database** | MySQL 8.0 |
| **Frontend** | HTML5, CSS, JS |
| **Infra** | Docker, Docker Compose |
| **Proxy / LB** | Nginx + HTTPS (Let's Encrypt) |
| **CI/CD** | GitHub Actions + Docker Hub + SSH 자동 배포 |
| **Cloud Infra** | Kakao Cloud VM + Bastion + AppSvr + Private DB |
| **Logging** | /home/ubuntu/ocr_project/logs (배포 로그 저장소) |

---

## 🏗️ 디렉토리 구조

```bash
ocr_project/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   ├── static/
│   │   └── uploads/
│   └── templates/
│       ├── layout.html
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard_home.html
│       ├── collections.html
│       ├── add_collection.html
│       ├── upload.html
│       └── list.html
│
├── nginx/
│   └── nginx.conf
│
├── logs/
│   └── deploy_update.log
│
├── deploy_update.sh
├── docker-compose.yml
└── .github/
    └── workflows/
        └── docker-ci.yml
```

---

## ⚙️ 환경 구성

### 🔧 .env (환경 변수)
```bash
DB_HOST=(DB PRIVATE IP)
DB_USER=(DB USER NAME)
DB_PASSWORD=(DB PASSWORD)
DB_NAME=(DB NAME)
SECRET_KEY=(SECRET_KEY)
```

### 🧱 Docker Compose (요약)
```yaml
services:
  ocr_app1~3:
    image: juin925/ocr_project:latest
    ports:
      - "5000:5000" / "5001:5000" / "5002:5000"
    command: gunicorn -w 4 -b 0.0.0.0:5000 app:app
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
```

---

## ⚙️ CI/CD 파이프라인

### 📄 `.github/workflows/docker-ci.yml`
```yaml
name: Build, Push, and Deploy

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build & Push
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile
          push: true
          tags: juin925/ocr_project:latest

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1.2.0
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /home/ubuntu
            ./deploy_update.sh
```

### 📜 `deploy_update.sh`
```bash
#!/bin/bash
LOG_DIR="/home/ubuntu/ocr_project/logs"
mkdir -p $LOG_DIR

echo "🔄 [$(date)] Deploy script started" >> $LOG_DIR/deploy_update.log
sudo docker pull juin925/ocr_project:latest >> $LOG_DIR/deploy_update.log 2>&1
cd /home/ubuntu/ocr_project
sudo docker compose down >> $LOG_DIR/deploy_update.log 2>&1
sudo docker compose up -d >> $LOG_DIR/deploy_update.log 2>&1
echo "✅ [$(date)] Deploy completed" >> $LOG_DIR/deploy_update.log
```

---

## 🔒 보안 및 인증서 구성

| 항목 | 내용 |
|------|------|
| **HTTPS 적용** | Certbot + Let's Encrypt |
| **도메인** | `juin.kakaolab.cloud` |
| **SSL 경로** | `/etc/letsencrypt/live/juin.kakaolab.cloud/` |
| **자동 갱신** | `certbot renew` (cron 자동화) |

---

## 🌍 향후 계획
| 단계 | 목표 |
|------|------|
| ☁️ **1단계** | Kubernetes로 Flask 컨테이너 오토스케일링 |
| 🔗 **2단계** | Prometheus + Grafana 로 리소스 모니터링 |
| 🧩 **3단계** | Kakao Cloud 멀티존 배포 실험 |

---

**아직 진행되고 있는 미완료 프로젝트이므로 추가되는대로 README.md 업데이트 예정**

---

## 👨‍💻 개발자
**Hwang Juin (황주인)**  
📧 juin925@gmail.com  
🌐 [juin.kakaolab.cloud](http://juin.kakaolab.cloud)  
💼 관심 분야: Cloud Engineering · DevOps  
