@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   빠른 Git Push (Vercel 자동 배포)
echo ========================================
echo.

REM Git 저장소 확인
if not exist .git (
    echo [오류] Git 저장소가 초기화되지 않았습니다.
    echo.
    echo 먼저 'git-setup.bat' 파일을 실행하세요!
    echo.
    pause
    exit /b 1
)

echo [1단계] 변경된 파일 확인 중...
echo.
git status --short
echo.

set /p confirm="위 파일들을 푸시하시겠습니까? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo 취소되었습니다.
    pause
    exit /b
)

echo.
echo [2단계] 파일 추가 중...
git add .

echo.
echo [3단계] 커밋 메시지 입력
set /p commit_msg="커밋 메시지 (엔터: 'Update'): "
if "%commit_msg%"=="" set commit_msg=Update

git commit -m "%commit_msg%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [알림] 변경사항이 없거나 커밋에 실패했습니다.
    echo.
    pause
    exit /b
)

echo.
echo [4단계] GitHub에 푸시 중...
git push

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   ✅ 성공! GitHub에 푸시되었습니다!
    echo ========================================
    echo.
    echo 🚀 Vercel에서 자동으로 배포 중입니다...
    echo.
    echo 배포 상태 확인:
    echo https://vercel.com/dashboard
    echo.
    echo 1-2분 후 웹사이트가 업데이트됩니다!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo   ⚠️ 푸시 실패
    echo ========================================
    echo.
    echo 가능한 원인:
    echo 1. 인터넷 연결 확인
    echo 2. GitHub 인증 확인 (토큰 또는 GitHub Desktop)
    echo 3. Remote 저장소 설정 확인: git remote -v
    echo ========================================
)

echo.
pause

