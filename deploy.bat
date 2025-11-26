@echo off
chcp 65001 >nul
echo ========================================
echo   SRT 자막 번역기 - Vercel 배포
echo ========================================
echo.
echo 이 스크립트는 Vercel에 배포를 시작합니다.
echo.
echo 배포 방법을 선택하세요:
echo.
echo 1. 테스트 배포 (미리보기)
echo 2. 프로덕션 배포 (실제 배포)
echo 3. 로그인만 하기
echo 4. 취소
echo.
set /p choice="선택 (1-4): "

if "%choice%"=="1" goto test_deploy
if "%choice%"=="2" goto prod_deploy
if "%choice%"=="3" goto login_only
if "%choice%"=="4" goto cancel

:test_deploy
echo.
echo 테스트 배포를 시작합니다...
echo.
npx vercel
goto end

:prod_deploy
echo.
echo 프로덕션 배포를 시작합니다...
echo.
npx vercel --prod
goto end

:login_only
echo.
echo Vercel 로그인을 시작합니다...
echo.
npx vercel login
goto end

:cancel
echo.
echo 배포가 취소되었습니다.
goto end

:end
echo.
echo ========================================
echo   배포 완료!
echo ========================================
echo.
echo 배포된 URL을 확인하세요.
echo 문제가 있다면 DEPLOY.md 파일을 참고하세요.
echo.
pause

