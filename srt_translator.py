"""
SRT 자막 파일 다국어 번역 프로그램
GPT API를 사용하여 한글 자막을 여러 언어로 번역합니다.
"""

import os
import re
from typing import List, Tuple
from openai import OpenAI


class SRTBlock:
    """SRT 파일의 각 블록을 나타내는 클래스"""
    
    def __init__(self, index: int, timecode: str, text: str):
        """
        Args:
            index: 블록 번호
            timecode: 타임코드 (예: 00:00:01,000 --> 00:00:03,000)
            text: 대사 텍스트
        """
        self.index = index
        self.timecode = timecode
        self.text = text
    
    def __str__(self):
        """SRT 형식으로 문자열 변환"""
        return f"{self.index}\n{self.timecode}\n{self.text}\n"


class SRTParser:
    """SRT 파일을 파싱하고 생성하는 클래스"""
    
    @staticmethod
    def parse(srt_content: str) -> List[SRTBlock]:
        """
        SRT 파일 내용을 파싱하여 SRTBlock 리스트로 반환
        
        Args:
            srt_content: SRT 파일의 전체 내용
            
        Returns:
            SRTBlock 객체들의 리스트
        """
        blocks = []
        # SRT 블록은 빈 줄로 구분됨
        raw_blocks = srt_content.strip().split('\n\n')
        
        for raw_block in raw_blocks:
            lines = raw_block.strip().split('\n')
            if len(lines) >= 3:
                # 첫 번째 줄: 블록 번호
                index = int(lines[0].strip())
                # 두 번째 줄: 타임코드
                timecode = lines[1].strip()
                # 나머지 줄: 대사 (여러 줄일 수 있음)
                text = '\n'.join(lines[2:])
                
                blocks.append(SRTBlock(index, timecode, text))
        
        return blocks
    
    @staticmethod
    def generate(blocks: List[SRTBlock]) -> str:
        """
        SRTBlock 리스트를 SRT 파일 형식의 문자열로 변환
        
        Args:
            blocks: SRTBlock 객체들의 리스트
            
        Returns:
            SRT 형식의 문자열
        """
        return '\n'.join(str(block) for block in blocks)


class GPTTranslator:
    """GPT API를 사용한 번역 클래스"""
    
    # 지원 언어 코드와 이름 매핑
    LANGUAGES = {
        'en': 'English',
        'ja': 'Japanese',
        'th': 'Thai',
        'zh': 'Chinese (Simplified)',
        'id': 'Indonesian',
        'es': 'Spanish'
    }
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenAI API 키
        """
        self.client = OpenAI(api_key=api_key)
    
    def translate_text(self, text: str, target_language: str) -> str:
        """
        단일 텍스트를 목표 언어로 번역
        
        Args:
            text: 번역할 텍스트 (한글)
            target_language: 목표 언어 이름 (예: 'English', 'Japanese')
            
        Returns:
            번역된 텍스트
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # 빠르고 저렴한 모델 사용
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the given Korean text to {target_language}. Only provide the translation without any additional explanation or notes. Maintain the tone and style of the original text."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=0.3,  # 일관성 있는 번역을 위해 낮은 temperature 사용
            )
            
            translated_text = response.choices[0].message.content.strip()
            return translated_text
            
        except Exception as e:
            print(f"번역 오류 발생: {e}")
            return text  # 오류 시 원본 텍스트 반환
    
    def translate_srt_blocks(self, blocks: List[SRTBlock], target_lang_code: str, verbose: bool = True) -> List[SRTBlock]:
        """
        SRT 블록들을 목표 언어로 번역
        
        Args:
            blocks: 원본 SRTBlock 리스트
            target_lang_code: 목표 언어 코드 (예: 'en', 'ja')
            verbose: 진행 상황을 출력할지 여부 (기본값: True)
            
        Returns:
            번역된 SRTBlock 리스트
        """
        target_language = self.LANGUAGES.get(target_lang_code, 'English')
        translated_blocks = []
        
        total = len(blocks)
        if verbose:
            print(f"\n{target_language} 번역 시작... (총 {total}개 블록)")
        
        for i, block in enumerate(blocks, 1):
            # 진행률 표시
            if verbose:
                print(f"  진행: {i}/{total} ({i*100//total}%)", end='\r')
            
            # 대사만 번역 (블록 번호와 타임코드는 유지)
            translated_text = self.translate_text(block.text, target_language)
            translated_blocks.append(
                SRTBlock(block.index, block.timecode, translated_text)
            )
        
        if verbose:
            print(f"  진행: {total}/{total} (100%) - 완료!")
        return translated_blocks


class SRTTranslatorApp:
    """SRT 번역 애플리케이션 메인 클래스"""
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenAI API 키
        """
        self.translator = GPTTranslator(api_key)
    
    def translate_file(self, input_file: str, output_dir: str = None):
        """
        SRT 파일을 여러 언어로 번역하여 각각 저장
        
        Args:
            input_file: 입력 SRT 파일 경로 (한글)
            output_dir: 출력 디렉토리 (기본값: 입력 파일과 동일한 디렉토리)
        """
        # 입력 파일 읽기
        print(f"\n입력 파일 읽는 중: {input_file}")
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                srt_content = f.read()
        except FileNotFoundError:
            print(f"오류: 파일을 찾을 수 없습니다 - {input_file}")
            return
        except Exception as e:
            print(f"파일 읽기 오류: {e}")
            return
        
        # SRT 파싱
        blocks = SRTParser.parse(srt_content)
        print(f"총 {len(blocks)}개의 자막 블록을 찾았습니다.")
        
        # 출력 디렉토리 설정
        if output_dir is None:
            output_dir = os.path.dirname(input_file) or '.'
        
        # 출력 디렉토리가 없으면 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # 입력 파일명에서 확장자 제거
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        
        # 각 언어로 번역 및 저장
        for lang_code, lang_name in self.translator.LANGUAGES.items():
            print(f"\n{'='*50}")
            print(f"{lang_name} 번역 작업 시작")
            print(f"{'='*50}")
            
            # 번역 수행
            translated_blocks = self.translator.translate_srt_blocks(blocks, lang_code)
            
            # SRT 형식으로 변환
            translated_srt = SRTParser.generate(translated_blocks)
            
            # 파일 저장
            output_file = os.path.join(output_dir, f"{base_name}_{lang_code}.srt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_srt)
            
            print(f"✓ 저장 완료: {output_file}")
        
        print(f"\n{'='*50}")
        print("모든 번역이 완료되었습니다!")
        print(f"{'='*50}")


def main():
    """메인 함수 - 프로그램 실행"""
    print("="*50)
    print("SRT 자막 파일 다국어 번역 프로그램")
    print("="*50)
    
    # API 키 입력받기
    api_key = input("\nOpenAI API 키를 입력하세요: ").strip()
    
    if not api_key:
        print("오류: API 키가 입력되지 않았습니다.")
        return
    
    # 입력 파일 경로 입력받기
    input_file = input("번역할 SRT 파일 경로를 입력하세요: ").strip()
    
    # 따옴표 제거 (드래그 앤 드롭 시 따옴표가 포함될 수 있음)
    input_file = input_file.strip('"').strip("'")
    
    if not os.path.exists(input_file):
        print(f"오류: 파일을 찾을 수 없습니다 - {input_file}")
        return
    
    # 출력 디렉토리 입력받기 (선택사항)
    output_dir = input("출력 디렉토리 (엔터 시 입력 파일과 동일한 위치): ").strip()
    output_dir = output_dir.strip('"').strip("'") if output_dir else None
    
    # 번역 실행
    app = SRTTranslatorApp(api_key)
    app.translate_file(input_file, output_dir)


if __name__ == "__main__":
    main()

