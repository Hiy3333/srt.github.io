@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   Git 저장소 설정 및 GitHub 푸시
echo ========================================
echo.
echo 현재 폴더: %CD%
echo.

REM .git 폴더가 있는지 확인
if exist .git (
    echo [정보] Git 저장소가 이미 존재합니다.
) else (
    echo [1단계] Git 저장소 초기화 중...
    git init
    echo.
)

echo [2단계] 파일 추가 중...
git add .
echo.

echo [3단계] 커밋 생성 중...
set /p commit_msg="커밋 메시지 입력 (엔터: 기본 메시지): "
if "%commit_msg%"=="" set commit_msg=Add SRT translator with animations

git commit -m "%commit_msg%"
echo.

echo [4단계] GitHub 저장소 URL 입력
echo.
echo GitHub에서 새 저장소를 만드신 후, 저장소 URL을 입력하세요.
echo 예: https://github.com/username/srt-translator.git
echo.
set /p repo_url="GitHub 저장소 URL: "

if "%repo_url%"=="" (
    echo.
    echo [오류] 저장소 URL을 입력하지 않았습니다.
    echo.
    echo ========================================
    echo   수동으로 아래 명령어를 실행하세요:
    echo ========================================
    echo git remote add origin [저장소URL]
    echo git branch -M main
    echo git push -u origin main
    echo ========================================
    pause
    exit /b
)

echo.
echo [5단계] Remote 저장소 설정 중...
git remote remove origin 2>nul
git remote add origin %repo_url%
git branch -M main
echo.

echo [6단계] GitHub에 푸시 중...
echo.
git push -u origin main
echo.

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   ✅ 성공! GitHub에 푸시되었습니다!
    echo ========================================
    echo.
    echo 이제 Vercel과 GitHub를 연결하세요:
    echo.
    echo 1. https://vercel.com/dashboard 접속
    echo 2. "New Project" 클릭
    echo 3. GitHub 저장소 선택: %repo_url%
    echo 4. "Deploy" 클릭
    echo.
    echo 이후부터는 'git push'만 하면
    echo Vercel에 자동으로 배포됩니다! 🚀
    echo ========================================
) else (
    echo.
    echo ========================================
    echo   ⚠️ 푸시 실패
    echo ========================================
    echo.
    echo 아래 사항을 확인하세요:
    echo.
    echo 1. Git이 설치되어 있나요?
    echo    https://git-scm.com/download/win
    echo.
    echo 2. GitHub 인증 설정이 되어 있나요?
    echo    - GitHub Desktop 사용
    echo    - 또는 Personal Access Token 설정
    echo.
    echo 3. 저장소 URL이 정확한가요?
    echo    입력한 URL: %repo_url%
    echo ========================================
)

echo.
pause

