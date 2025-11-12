# 📘 Book OCR & English Translation Service  
AI 기반 책 이미지 OCR + 자동 번역 시스템  

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey)
![EasyOCR](https://img.shields.io/badge/EasyOCR-Text%20Recognition-orange)
![Googletrans](https://img.shields.io/badge/Googletrans-Auto%20Translation-green)
![MySQL](https://img.shields.io/badge/Database-MySQL-blue)
![Docker](https://img.shields.io/badge/Container-Docker-informational)
![Kubernetes](https://img.shields.io/badge/Deployment-Kubernetes-lightblue)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 📖 목차
1. [프로젝트 개요](#-프로젝트-개요)
2. [주요 기능](#-주요-기능)
3. [기술 스택](#-기술-스택)
4. [프로젝트 구조](#-프로젝트-구조)
5. [환경 설정](#-환경-설정)
6. [Docker 실행법](#-docker-실행법)
7. [API 라우트](#-api-라우트)
8. [보안 설계](#-보안-설계)
9. [향후 계획](#-향후-계획)
10. [개발자](#-개발자)

---

## 📖 프로젝트 개요
이 서비스는 **사용자가 촬영하거나 스캔한 책 이미지를 업로드하면**,  
AI 기반 **OCR 기술(EasyOCR)** 로 텍스트를 추출하고 **Googletrans API**를 사용하여 영어로 번역하는 **웹 기반 번역 플랫폼**입니다.

> 🎯 목표:  
> - 수작업 번역 시간을 줄이고,  
> - 시각적으로 불편한 사용자도 책 내용을 손쉽게 접근하도록 돕는 것.

---

## 🚀 주요 기능

| 기능 | 설명 |
|------|------|
| 🧠 **OCR 텍스트 인식** | EasyOCR을 사용해 이미지 내 한글 텍스트 추출 |
| 🌐 **자동 번역** | Googletrans로 영어 번역 수행 |
| 📤 **이미지 업로드** | 책/문서 이미지 업로드 및 미리보기 |
| 📚 **컬렉션 관리** | 책 단위로 이미지 그룹화 및 저장 |
| ✏️ **OCR 결과 수정** | 인식된 텍스트를 사용자가 직접 편집 가능 |
| 💾 **DB 저장** | 이미지, 텍스트, 번역 결과를 MySQL DB에 저장 |
| 🔒 **사용자 관리** | 회원가입, 로그인, 세션 유지 |
| ☁️ **배포 준비 완료** | Docker 기반 클라우드 배포 (Kubernetes 확장 예정) |

---

## 🧩 기술  스택

| 구분 | 사용 기술 |
|------|-------------|
| **Backend** | Flask (Python 3.10) |
| **OCR Engine** | EasyOCR |
| **Translation** | Googletrans |
| **Database** | MySQL 8.0 |
| **Frontend** | HTML / CSS (Jinja2 템플릿) |
| **Infra** | Docker, Docker Compose |
| **Cloud (Next)** | Kakao Cloud / AWS (Kubernetes 예정) |

---

## 🏗️ 프로젝트 구조

ocr_project/
├── backend/
│ ├── app.py
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── .env
│ ├── static/
│ │ └── uploads/
│ └── templates/
│ ├── layout.html
│ ├── home.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard_home.html
│ ├── collections.html
│ ├── add_collection.html
│ ├── upload.html
│ └── list.html
└── docker-compose.yml
