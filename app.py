"""
SRT 자막 파일 다국어 번역 웹 애플리케이션
Flask 기반 웹 인터페이스
"""

import os
import io
import zipfile
import re
from datetime import datetime
from flask import Flask, render_template, request, send_file, jsonify, session
from werkzeug.utils import secure_filename
from srt_translator import SRTParser, GPTTranslator, SRTBlock

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 최대 파일 크기
app.config['SECRET_KEY'] = 'srt-translator-secret-key-2024'

# 작업 폴더 경로 설정
FOLDERS = {
    '1-2': '1-2. SRT 파일 복제 (다국어 파일 생성)',
    '2-1': '2-1. 단어 수정',
    '2-2': '2-2. 화자명 전체 변경 (파일 전체에서 이름 치환)',
    '3-1': '3-1. 화자명 변경된 번역'
}

# 폴더 생성
for folder in FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

# 지원 언어 목록
LANGUAGES = {
    'en': 'English (영어)',
    'ja': 'Japanese (일본어)',
    'th': 'Thai (태국어)',
    'zh': 'Chinese (중국어)',
    'id': 'Indonesian (인도네시아어)',
    'es': 'Spanish (스페인어)'
}


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html', languages=LANGUAGES)


@app.route('/translate', methods=['POST'])
def translate():
    """SRT 파일 번역 처리"""
    try:
        # API 키 확인
        api_key = request.form.get('api_key')
        if not api_key:
            return jsonify({'error': 'API 키를 입력해주세요.'}), 400
        
        # 파일 확인
        if 'srt_file' not in request.files:
            return jsonify({'error': 'SRT 파일을 업로드해주세요.'}), 400
        
        file = request.files['srt_file']
        if file.filename == '':
            return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
        
        if not file.filename.endswith('.srt'):
            return jsonify({'error': 'SRT 파일만 업로드 가능합니다.'}), 400
        
        # 선택된 언어 확인
        selected_languages = request.form.getlist('languages')
        if not selected_languages:
            return jsonify({'error': '최소 하나의 언어를 선택해주세요.'}), 400
        
        # 파일 읽기
        srt_content = file.read().decode('utf-8')
        
        # SRT 파싱
        blocks = SRTParser.parse(srt_content)
        if not blocks:
            return jsonify({'error': 'SRT 파일을 파싱할 수 없습니다. 파일 형식을 확인해주세요.'}), 400
        
        # 번역기 초기화
        translator = GPTTranslator(api_key)
        
        # 메모리에 ZIP 파일 생성
        zip_buffer = io.BytesIO()
        
        # 원본 파일명 (확장자 제거)
        original_filename = os.path.splitext(secure_filename(file.filename))[0]
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # 선택된 언어별로 번역
            for lang_code in selected_languages:
                if lang_code not in LANGUAGES:
                    continue
                
                # 번역 수행 (웹 버전에서는 verbose=False)
                translated_blocks = translator.translate_srt_blocks(blocks, lang_code, verbose=False)
                
                # SRT 형식으로 변환
                translated_srt = SRTParser.generate(translated_blocks)
                
                # ZIP 파일에 추가
                filename = f"{original_filename}_{lang_code}.srt"
                zip_file.writestr(filename, translated_srt)
        
        # ZIP 파일을 전송 준비
        zip_buffer.seek(0)
        
        # 다운로드 파일명 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        download_filename = f"{original_filename}_translated_{timestamp}.zip"
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=download_filename
        )
    
    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500


@app.route('/convert_txt_to_srt', methods=['POST'])
def convert_txt_to_srt():
    """TXT 파일을 SRT 형식으로 변환 (1-1 단계)"""
    try:
        # 파일 확인
        if 'txt_file' not in request.files:
            return jsonify({'error': 'TXT 파일을 업로드해주세요.'}), 400
        
        file = request.files['txt_file']
        if file.filename == '':
            return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
        
        # 파일 읽기
        txt_content = file.read().decode('utf-8')
        
        # TXT를 SRT 형식으로 변환
        # 간단한 변환: 각 줄을 자막 블록으로 만들기
        lines = [line.strip() for line in txt_content.split('\n') if line.strip()]
        
        srt_content = ""
        for i, line in enumerate(lines, 1):
            # 각 자막은 2초 간격으로 배치 (시작 시간 기준)
            start_seconds = (i - 1) * 2
            end_seconds = start_seconds + 2
            
            start_time = f"{start_seconds // 3600:02d}:{(start_seconds % 3600) // 60:02d}:{start_seconds % 60:02d},000"
            end_time = f"{end_seconds // 3600:02d}:{(end_seconds % 3600) // 60:02d}:{end_seconds % 60:02d},000"
            
            srt_content += f"{i}\n{start_time} --> {end_time}\n{line}\n\n"
        
        # 파일명 생성
        output_filename = os.path.splitext(secure_filename(file.filename))[0] + '.srt'
        
        # 1-2 폴더에 저장
        output_path = os.path.join(FOLDERS['1-2'], output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        return jsonify({
            'success': True,
            'content': srt_content,
            'filename': output_filename,
            'saved_to': FOLDERS['1-2']
        })
    
    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500


@app.route('/duplicate_srt', methods=['POST'])
def duplicate_srt():
    """SRT 파일 복제 (1-2 단계)"""
    try:
        data = request.get_json()
        
        # 1-1에서 전달받은 파일 또는 새로 업로드된 파일 처리
        srt_content = data.get('content', '')
        filename = data.get('filename', 'duplicated.srt')
        count = int(data.get('count', 1))
        
        if not srt_content:
            return jsonify({'error': 'SRT 내용이 없습니다.'}), 400
        
        # 복제된 파일들을 생성하고 2-1 폴더에 저장
        duplicated_files = []
        for i in range(count):
            dup_filename = f"{os.path.splitext(filename)[0]}_copy{i+1}.srt"
            
            # 2-1 폴더에 저장
            output_path = os.path.join(FOLDERS['2-1'], dup_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            duplicated_files.append({
                'filename': dup_filename,
                'content': srt_content
            })
        
        return jsonify({
            'success': True,
            'files': duplicated_files,
            'saved_to': FOLDERS['2-1']
        })
    
    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500


@app.route('/replace_words', methods=['POST'])
def replace_words():
    """SRT 파일에서 단어 수정 (2-1 단계)"""
    try:
        data = request.get_json()
        
        # 1-2에서 전달받은 파일 또는 새로 업로드된 파일 처리
        srt_content = data.get('content', '')
        filename = data.get('filename', 'modified.srt')
        replacements = data.get('replacements', [])
        
        if not srt_content:
            return jsonify({'error': 'SRT 내용이 없습니다.'}), 400
        
        # 단어 교체 수행
        modified_content = srt_content
        replacement_count = {}
        
        for replacement in replacements:
            old_word = replacement.get('old', '')
            new_word = replacement.get('new', '')
            
            if old_word:
                count = modified_content.count(old_word)
                modified_content = modified_content.replace(old_word, new_word)
                replacement_count[old_word] = count
        
        # 결과 파일명 생성
        result_filename = f"{os.path.splitext(filename)[0]}_modified.srt"
        
        # 2-2 폴더에 저장
        output_path = os.path.join(FOLDERS['2-2'], result_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        return jsonify({
            'success': True,
            'content': modified_content,
            'filename': result_filename,
            'replacement_count': replacement_count,
            'saved_to': FOLDERS['2-2']
        })
    
    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500


@app.route('/replace_speaker_names', methods=['POST'])
def replace_speaker_names():
    """화자명 전체 변경 (2-2 단계)"""
    try:
        data = request.get_json()
        
        srt_content = data.get('content', '')
        filename = data.get('filename', 'speaker_changed.srt')
        replacements = data.get('replacements', [])
        
        if not srt_content:
            return jsonify({'error': 'SRT 내용이 없습니다.'}), 400
        
        # 화자명 교체 수행
        modified_content = srt_content
        replacement_count = {}
        
        for replacement in replacements:
            old_name = replacement.get('old', '')
            new_name = replacement.get('new', '')
            
            if old_name:
                # 화자명 패턴 찾기 (예: "화자명:" 형식)
                count = modified_content.count(old_name)
                modified_content = modified_content.replace(old_name, new_name)
                replacement_count[old_name] = count
        
        # 결과 파일명 생성
        result_filename = f"{os.path.splitext(filename)[0]}_speaker_changed.srt"
        
        # 3-1 폴더에 저장
        output_path = os.path.join(FOLDERS['3-1'], result_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        return jsonify({
            'success': True,
            'content': modified_content,
            'filename': result_filename,
            'replacement_count': replacement_count,
            'saved_to': FOLDERS['3-1']
        })
    
    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500


@app.route('/health')
def health():
    """서버 상태 확인"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 SRT 자막 번역 웹 서비스 시작")
    print("="*60)
    print("\n웹 브라우저에서 다음 주소로 접속하세요:")
    print("👉 http://localhost:5000")
    print("\n서버를 종료하려면 Ctrl+C를 누르세요.")
    print("="*60 + "\n")
    
    # 개발 모드로 실행
    app.run(debug=True, host='0.0.0.0', port=5000)

