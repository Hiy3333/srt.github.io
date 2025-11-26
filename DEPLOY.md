# 🚀 SRT 자막 번역기 - Vercel 배포 가이드

## ✅ 배포 준비 완료!

애니메이션 효과가 추가된 `index.html` 파일과 Vercel 배포 설정이 모두 준비되었습니다.

## 📋 추가된 애니메이션 효과

### 1. 페이지 로드 애니메이션
- ✨ 헤더 타이틀 바운스 효과
- ✨ 서브타이틀 슬라이드 인 효과
- ✨ 탭 네비게이션 페이드 인
- ✨ 컨테이너 페이드업 효과

### 2. 인터랙티브 호버 효과
- 🎯 모든 버튼에 리플 효과 추가
- 🎯 입력 필드 포커스 시 확대 애니메이션
- 🎯 파일 업로드 영역 드래그 앤 드롭 효과
- 🎯 언어 선택 체크박스 체크 애니메이션
- 🎯 라벨 호버 시 슬라이드 효과

### 3. 진행 상태 애니메이션
- ⚡ 프로그레스 바 shimmer 효과
- ⚡ 타이머 펄스 효과
- ⚡ 스피너 글로우 효과
- ⚡ 에러 메시지 shake 애니메이션
- ⚡ 일시정지 알림 깜빡임 효과

### 4. 스크롤 애니메이션
- 📜 폼 섹션 스크롤 시 순차적 페이드 인
- 📜 Intersection Observer를 활용한 부드러운 등장

### 5. 버튼 효과
- 🔘 클릭 시 스케일 애니메이션
- 🔘 호버 시 그림자 효과
- 🔘 삭제 버튼 회전 효과
- 🔘 추가 버튼 빛나는 효과

## 🚀 Vercel 배포 방법

### 방법 1: Vercel CLI 사용 (권장)

#### 1단계: 로그인
```bash
npx vercel login
```
- 이메일 주소 입력
- 이메일로 받은 인증 링크 클릭

#### 2단계: 배포 (테스트)
```bash
npx vercel
```
- 질문에 답변:
  - Set up and deploy? → **Y**
  - Which scope? → 본인 계정 선택
  - Link to existing project? → **N**
  - What's your project's name? → **srt-translator** (또는 원하는 이름)
  - In which directory is your code located? → **./** (엔터)

#### 3단계: 프로덕션 배포
```bash
npx vercel --prod
```

### 방법 2: Vercel 웹사이트 사용

#### 1단계: GitHub에 푸시 (선택사항)
```bash
git init
git add .
git commit -m "Add SRT translator with animations"
git branch -M main
git remote add origin https://github.com/your-username/srt-translator.git
git push -u origin main
```

#### 2단계: Vercel에서 배포
1. [Vercel Dashboard](https://vercel.com/dashboard) 접속
2. "New Project" 클릭
3. GitHub 저장소 연결 또는 "Import Third-Party Git Repository"
4. 프로젝트 설정:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (비워두기)
   - **Output Directory**: (비워두기)
5. "Deploy" 클릭

### 방법 3: 파일 직접 업로드

1. [Vercel Dashboard](https://vercel.com/dashboard) 접속
2. "Add New..." → "Project" 클릭
3. "Deploy from Template" 대신 "Import Git Repository" 건너뛰기
4. 파일 드래그 앤 드롭 또는 폴더 선택
5. 다음 파일들을 포함:
   - `index.html` ✅
   - `vercel.json` ✅
   - `.gitignore` ✅

## 📁 배포에 필요한 파일

현재 프로젝트에 다음 파일들이 준비되어 있습니다:

- ✅ `index.html` - 메인 웹 애플리케이션 (애니메이션 효과 포함)
- ✅ `vercel.json` - Vercel 배포 설정
- ✅ `.gitignore` - Git 제외 파일 목록
- ✅ `README_VERCEL.md` - 상세 배포 가이드

## 🎉 배포 완료 후

배포가 완료되면 다음과 같은 URL을 받게 됩니다:
```
https://your-project-name.vercel.app
```

또는 커스텀 도메인을 연결할 수 있습니다.

## 🔧 주요 기능

1. **TXT → SRT 변환**: 텍스트 파일을 자막 파일로 변환
2. **SRT 파일 복제**: 다국어 번역을 위한 파일 생성
3. **단어 수정**: 특정 단어를 일괄 변경
4. **화자명 변경 번역**: GPT를 사용한 화자별 번역
5. **전체 번역**: 여러 언어로 동시 번역
6. **프리미어 자막 변환**: 프리미어 프로 자막을 SRT로 변환

## 💡 사용 팁

### API 키 설정
- OpenAI API 키는 브라우저의 localStorage에 안전하게 저장됩니다
- 서버에 전송되지 않으므로 보안상 안전합니다
- API 키 발급: https://platform.openai.com/api-keys

### 드래그 앤 드롭
- 모든 파일 업로드 영역에서 드래그 앤 드롭이 가능합니다
- 여러 파일을 한 번에 드래그하여 업로드할 수 있습니다

### 애니메이션 커스터마이징
`index.html`의 CSS 섹션에서 애니메이션을 수정할 수 있습니다:
- 애니메이션 속도 조절
- 색상 변경
- 효과 추가/제거

## 🌐 브라우저 지원

- ✅ Chrome (최신 버전)
- ✅ Firefox (최신 버전)
- ✅ Safari (최신 버전)
- ✅ Edge (최신 버전)
- ✅ 모바일 브라우저

## 📱 반응형 디자인

모든 화면 크기에서 최적화된 UI를 제공합니다:
- 📱 모바일 (320px ~)
- 📱 태블릿 (768px ~)
- 💻 데스크톱 (1024px ~)

## 🆘 문제 해결

### 배포 실패 시
1. `vercel.json` 파일이 프로젝트 루트에 있는지 확인
2. `index.html` 파일이 루트 디렉토리에 있는지 확인
3. Vercel CLI 재설치: `npm install -g vercel@latest`

### 애니메이션이 작동하지 않을 때
1. 브라우저 캐시 삭제
2. 하드 리프레시 (Ctrl + Shift + R 또는 Cmd + Shift + R)
3. 브라우저 개발자 도구에서 콘솔 오류 확인

### API 키 관련
- API 키가 저장되지 않으면 브라우저 쿠키 설정 확인
- 시크릿 모드에서는 localStorage가 제한될 수 있습니다

## 📞 지원

- Vercel 문서: https://vercel.com/docs
- OpenAI API 문서: https://platform.openai.com/docs

## 🎊 완료!

모든 준비가 완료되었습니다. 위의 방법 중 하나를 선택하여 배포를 진행하세요!

배포 후 URL을 공유하면 누구나 웹 브라우저에서 SRT 자막 번역기를 사용할 수 있습니다. 🚀
