# SRT 자막 번역기 - Vercel 배포 가이드

## 🚀 Vercel 배포 방법

### 1. Vercel 계정 준비
1. [Vercel](https://vercel.com) 웹사이트 방문
2. GitHub 계정으로 로그인

### 2. GitHub 저장소 생성 (선택사항)
프로젝트를 GitHub에 푸시하면 자동 배포가 가능합니다.

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### 3. Vercel CLI를 통한 배포

#### 3-1. Vercel CLI 설치
```bash
npm install -g vercel
```

#### 3-2. 로그인
```bash
vercel login
```

#### 3-3. 배포 실행
프로젝트 폴더에서 다음 명령어 실행:
```bash
vercel
```

첫 배포 시 몇 가지 질문이 나옵니다:
- Set up and deploy? → **Y**
- Which scope? → 본인 계정 선택
- Link to existing project? → **N**
- What's your project's name? → 원하는 이름 입력
- In which directory is your code located? → **./** (엔터)

#### 3-4. 프로덕션 배포
```bash
vercel --prod
```

### 4. Vercel 웹사이트를 통한 배포

1. [Vercel Dashboard](https://vercel.com/dashboard) 접속
2. "New Project" 클릭
3. GitHub 저장소 연결 또는 파일 직접 업로드
4. 프로젝트 설정:
   - Framework Preset: **Other**
   - Root Directory: **./** (기본값)
5. "Deploy" 클릭

### 5. 배포 완료 ✅

배포가 완료되면 다음과 같은 URL을 받게 됩니다:
```
https://your-project-name.vercel.app
```

## 📝 주요 파일 설명

- **index.html**: 메인 웹 애플리케이션
- **vercel.json**: Vercel 배포 설정 파일
- **.gitignore**: Git에서 제외할 파일 목록

## 🎨 추가된 애니메이션 효과

### 1. 페이지 로드 애니메이션
- 헤더 타이틀 바운스 효과
- 서브타이틀 슬라이드 인
- 탭 네비게이션 페이드 인
- 컨테이너 페이드업

### 2. 인터랙티브 효과
- 버튼 호버 시 리플 효과
- 입력 필드 포커스 애니메이션
- 파일 업로드 영역 드래그 앤 드롭 효과
- 언어 선택 체크박스 애니메이션

### 3. 진행 상태 애니메이션
- 프로그레스 바 shimmer 효과
- 타이머 펄스 효과
- 스피너 글로우 효과
- 에러 메시지 shake 애니메이션

### 4. 스크롤 애니메이션
- 폼 섹션 스크롤 시 페이드 인
- Intersection Observer를 활용한 부드러운 등장

## 🔧 커스터마이징

### 색상 변경
`index.html`의 CSS 변수를 수정하여 색상을 변경할 수 있습니다:
```css
/* 메인 그라데이션 색상 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### 애니메이션 속도 조절
```css
/* 애니메이션 지속 시간 변경 */
animation: fadeInUp 0.8s ease-out; /* 0.8s를 원하는 시간으로 변경 */
```

## 📱 반응형 디자인

모바일, 태블릿, 데스크톱 모든 기기에서 최적화된 UI를 제공합니다.

## 🌐 브라우저 지원

- Chrome (최신 버전)
- Firefox (최신 버전)
- Safari (최신 버전)
- Edge (최신 버전)

## 💡 팁

1. **무료 플랜**: Vercel 무료 플랜으로도 충분히 사용 가능합니다.
2. **자동 HTTPS**: Vercel이 자동으로 SSL 인증서를 제공합니다.
3. **커스텀 도메인**: Vercel 대시보드에서 커스텀 도메인을 연결할 수 있습니다.
4. **환경 변수**: OpenAI API 키는 브라우저에 저장되므로 환경 변수 설정이 필요 없습니다.

## 🆘 문제 해결

### 배포 실패 시
1. `vercel.json` 파일이 프로젝트 루트에 있는지 확인
2. `index.html` 파일이 루트 디렉토리에 있는지 확인
3. Vercel CLI를 최신 버전으로 업데이트: `npm install -g vercel@latest`

### API 키 관련
- API 키는 브라우저의 localStorage에 저장됩니다
- 서버에 저장되지 않으므로 보안상 안전합니다

## 📞 지원

문제가 발생하면 [Vercel 문서](https://vercel.com/docs)를 참조하세요.
