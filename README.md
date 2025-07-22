###### SKN13_4th_2TEAM
# 주제 : LLM을 연동한 사용자 맞춤 음악 추천 웹페이지 개발


## 📖 프로젝트 소개  

“당신의 감정, 날씨, 장소에 딱 맞는 음악을 추천합니다.”
>이 프로젝트는 사용자 상태(감정, 날씨)에 기반하여 가장 적절한 음악을 추천하는 AI 큐레이터 시스템입니다.
GPT 기반 LLM과 그리고 외부 음악 API들을 융합해 사용자 맞춤형 음악을 제안합니다.


# 🏷️ 목 차
1️⃣ [팀 소개](#1️⃣-팀-소개)

2️⃣ [프로젝트 개요](#2️⃣-프로젝트-개요)

3️⃣ [기술 스택 및 파일구조](#3️⃣-기술-스택)

4️⃣ [시스템 아키텍처](#4️⃣-시스템-아키텍처)

5️⃣ [화면 설계서](#5️⃣-화면-설계서)

6️⃣ [요구사항 명세서](#6️⃣-요구사항-명세서)

7️⃣ [수집한 데이터 및 전처리 요약](#7️⃣-수집한-데이터-및-전처리-요약)

8️⃣ [테스트 계획 및 결과 보고서](#8️⃣-테스트-계획-및-결과-보고서)

9️⃣ [성능 개선 노력](#9️⃣-성능-개선-노력) 

🔟 [추후 개선점](#-추후-개선점)

🔍 [한 줄 회고](#-한-줄-회고) 


## 1️⃣ 팀 소개
 ### 팀 명 : 
### 🗓️ 개발 기간
> 2025.07.18 ~ 2025.07.22
### 👥 팀원

<table width="100%">

  <tr>

  <tr>
    <td align="center" width="16%">
      <b></b>
    </td>
    <td align="center" width="16%">
      <b></b>
    </td>
    <td align="center" width="16%">
      <b></b>
    </td>
    <td align="center" width="16%">
      <b></b>
    <td align="center" width="16%">
      <b></b>
    <td align="center" width="16%">
      <b></b>
    </td>
  </tr>
  <tr>
    <td align="center" width="16%">
      <a href="https://github.com/Koojh99">
        <img src="https://img.shields.io/badge/GitHub-Koojh99-1F1F1F?logo=github" alt="구자현 GitHub"/>
      </a>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/Gogimin">
        <img src="https://img.shields.io/badge/GitHub-Gogimin-1F1F1F?logo=github" alt="김지민 GitHub"/>
      </a>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/rudwo524">
        <img src="https://img.shields.io/badge/GitHub-rudwo524-1F1F1F?logo=github" alt="민경재 GitHub"/>
      </a>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/subin0821">
        <img src="https://img.shields.io/badge/GitHub-subin0821-1F1F1F?logo=github" alt="박수빈 GitHub"/>
      </a>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/yunawawa">
       <img src="https://img.shields.io/badge/GitHub-yunawawa-1F1F1F?logo=github" alt="이유나 GitHub"/>
      </a>
    </td>
    <td align="center" width="16%">
      <a href="https://github.com/seonguihong">
        <img src="https://img.shields.io/badge/GitHub-Gogimin-1F1F1F?logo=github" alt="홍성의 GitHub"/>
      </a>
    </td>
  </tr>
</table>

## 2️⃣ 프로젝트 개요

<img src="./images/주제배경.png" width="70%" />

### ⭐ 프로젝트 필요성

**1. 감정 기반 음악 추천에 대한 수요 증가** <br>
현대 사용자들은 단순한 장르나 인기 순위보다 자신의 감정 상태에 어울리는 음악을 찾고자 합니다.<br>
특히, 스트레스 해소, 집중력 향상, 위로, 활력 증진 등의 목적을 가진 사용자들에게는 심리적 맥락에 맞는 음악 추천이 더욱 중요해지고 있습니다.

>❝ 나의 기분에 맞는 노래를 추천해주는 서비스는 없을까? ❞
❝ 지금 이 순간에 딱 맞는 음악이 듣고 싶어. ❞

**2. 기존 음악 추천의 한계**

| 기존 방식         | 한계점                                                       |
|------------------|-------------------------------------------------------------|
| 협업 필터링 기반    | 과거 청취 이력에 의존, 감정이나 현재 상황 같은 맥락 정보를 반영하기 어려움        |
| 장르 중심 추천      | 상황(예: 날씨, 위치, 기분) 등 외부 요인을 고려하지 못함                          |
| 무작위 큐레이션     | 추천 신뢰도가 낮아 사용자 만족도와 몰입도가 떨어질 수 있음                        |
<br>

**3. 정서적/환경적 맥락 인식의 필요성**
<br>
  음악은 사용자 감정과 밀접하게 연결된 콘텐츠입니다.<br>
   하지만 현재 대부분의 플랫폼은 정서적 맥락(예: 우울함, 설렘, 혼자 있는 시간)이나 환경적 요인(날씨, 위치 등)을 고려하지 않고 있습니다.

>본 프로젝트는 이러한 정서적 공감 기반 추천을 통해 사용자 경험(UX)을 한층 향상시키고자 합니다.
<br>

**4. 생성형 AI 기술을 활용한 차별화된 접근**
<br>
 최근 GPT 기반 생성형 AI는 사용자의 상태를 정밀하게 분석하고 자연스러운 언어로 추천 이유를 설명할 수 있습니다.

>본 프로젝트는 GPT와 결합하여 단순한 추천을 넘어 "이 음악이 당신에게 어울리는 이유"까지 설명하는 추천 시스템을 구현합니다.
<br>

### 🎯 프로젝트 목표

| 목표 항목             | 설명                                                              |
|----------------------|-------------------------------------------------------------------|
| 감정/날씨/위치 해석      | 사용자 입력을 기반으로 정서적·환경적 맥락을 LLM이 해석하도록 설계             |
| LLM 응답 생성           | 유사 곡 정보를 바탕으로 GPT가 자연어로 곡 추천과 설명을 생성                  |
| 감정 태그 자동화         | Last.fm 및 LLM을 활용해 곡별 감정 태그를 자동 수집 및 보완                   |
| 미리듣기 링크 연결        | Spotify/YouTube API를 이용해 실제 재생 가능한 트랙 링크 제공                 |



<hr>

## 3️⃣ 기술 스택 및 파일 구조
| 항목                | 내용 |
|---------------------|------|
| **Frontend**        |![HTML](https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white)<br>![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black)|
| **Backend**         |![Django](https://img.shields.io/badge/-Django-092E20?logo=django&logoColor=white) |
| **Language**        | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) |
| **Development**     | ![VS Code](https://img.shields.io/badge/-VS%20Code-007ACC?logo=visual-studio-code&logoColor=white) |
| **Crawler**         | ![BeautifulSoup](https://img.shields.io/badge/-BeautifulSoup-4B8BBE?logo=python&logoColor=white)<br>![Selenium](https://img.shields.io/badge/-Selenium-43B02A?logo=selenium&logoColor=white) |
| **Embedding**       |![openai](https://img.shields.io/badge/-openai-412991?logo=openai&logoColor=white)|
| **LLM Model**       | ![gpt-4.1](https://img.shields.io/badge/gpt--4.1-4B91FF?logo=openai&logoColor=white) |
| **Collaboration Tool** | ![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white) |
| **Vector DB**| ![Chroma](https://img.shields.io/badge/Chroma-ff5c83?logo=databricks&logoColor=white) |
| **API 활용** | ![OpenWeather](https://img.shields.io/badge/OpenWeather_API-FF9900?style=for-the-badge&logoColor=white) |

## 📁 프로젝트 폴더 구조

```
SKN13_4th_2team:
├─.ipynb_checkpoints
├─accounts
├─bot
├─chatbot
├─faq
├─forum
├─home
├─images
├─locale
├─media
├─music_project
├─mypage
├─scripts
├─search
├─static
└─templates

```


<hr>

## 4️⃣ 시스템 아키텍처





<hr>

## 5️⃣ 화면 설계서


<hr>

## 6️⃣ 요구사항 명세서


<hr>

## 7️⃣ 수집한 데이터 및 전처리 요약

> 본 시스템은 

1. **데이터 수집**




2. **문서화(Document화)**

  

3. **벡터 임베딩 및 저장소 구축**

  

4. **검색 및 RAG Tool 연동**

  

<hr>

## 8️⃣ 테스트 계획 및 결과 보고서
### 테스트 계획 및 결과 보고서

### ✅ 테스트 개요

- **테스트 목적**  
 
- **테스트 기간**

- **테스트 환경**  
  
  - **테스트 화면 구현**
  
  

### ✅ 테스트 항목 및 시나리오


### ✅ 테스트 결과 요약


<hr>

## 🚀 개발 히스토리 및 문제해결 과정



### 1️⃣ Kaggle 데이터셋 기반 추천 시스템 구현
- **설명:**  
  - Kaggle 공개 음악 데이터를 이용해 초기 추천 시스템 개발
- **문제점:**  
  - 데이터가 한정적  
  - 최신 음악 반영 불가  
- **결과:**  
  → 실제 서비스 활용성 한계



### 2️⃣ Spotify API 연동 음악 검색 기능
- **설명:**  
  - Spotify API를 활용해 실시간 곡 검색/추천 기능 구현
- **문제점:**  
  - 감정(기분) 기반 검색 미지원  
  - 추천 결과 신뢰성 낮음  
- **결과:**  
  → 사용자 만족도 저하



### 3️⃣ Last.fm API 태그 기반 검색 기능 도입
- **설명:**  
  - Last.fm API에서 제공하는 태그(감정/장르 등) 활용한 곡 추천 기능 추가
- **문제점:**  
  - 여러 태그 입력 시 일부만 반영  
  - 검색 결과 일관성 부족  
- **결과:**  
  → 복합 조건 추천 품질 한계



### 4️⃣ 태그 교집합 기반(AND) 필터링 로직 개선
- **설명:**  
  - 각 태그별 곡 리스트를 받아온 후  여러 태그의 **교집합(AND)** 만 추려내는 방식 도입
- **개선:**  
  - 사용자가 입력한 모든 태그 만족 곡만 추천
- **결과:**  
  → 맞춤형 추천 정확도 및 일관성 향상



### 5️⃣ 지역/날씨 기반 음악 추천 기능 추가
- **설명:**  
  - 외부 날씨 API와 연동, 지역/날씨별 맞춤 음악 추천 기능 구현
  - (예: “맑음” “비” “눈” 등 날씨 상황별 자동 태그 매핑)
- **의의:**  
  - 사용자 니즈(날씨별 음악 추천) 반영  
  - 상황에 어울리는 음악 경험 제공  
- **결과:**  
  → 실시간/상황 맞춤 추천 서비스 완성


## 🔟 추후 개선점



<hr>

## 🔍 한 줄 회고

| 팀원   | 한 줄 회고 내용 |
|--------|----------------|

