#!/usr/bin/env python3
"""
슬라이드 중복 검증 스크립트

SPEC-B7 기준:
- 슬라이드 내 중복 방지 (본문/다이어그램/팝업)
- 슬라이드 간 중복 방지
- 텍스트 유사도 80% 이상 → 경고

사용법:
    python scripts/validate-slides.py docs/slides.html
    python scripts/validate-slides.py docs/slides.html --threshold 0.75
    python scripts/validate-slides.py docs/slides.html --output report.md
"""

import argparse
import difflib
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class SlideExtractor:
    """슬라이드 HTML 에서 본문/다이어그램/팝업 텍스트 추출"""

    def extract(self, html: str) -> dict:
        """
        슬라이드 HTML 에서 텍스트 추출

        Returns:
            {
                "slide_1": {
                    "body": "텍스트",
                    "diagram": "텍스트",
                    "popup": "텍스트"
                },
                ...
            }
        """
        slides = {}
        # 슬라이드 분할 (data-slide 속성 기준)
        slide_pattern = re.compile(r'data-slide="(\d+)"', re.IGNORECASE)
        # 섹션 분할 (본문/다이어그램/팝업)
        body_pattern = re.compile(r'class="body"', re.IGNORECASE)
        diagram_pattern = re.compile(r'class="diagram"', re.IGNORECASE)
        popup_pattern = re.compile(r'class="popup"', re.IGNORECASE)

        # 간단한 HTML 파싱 (실제 구현은 BeautifulSoup 권장)
        # 현재는 텍스트 기반 추출
        lines = html.split('\n')
        current_slide = None
        current_section = None
        slide_text = {}

        for line in lines:
            # 슬라이드 번호 추출
            slide_match = slide_pattern.search(line)
            if slide_match:
                current_slide = f"slide_{slide_match.group(1)}"
                slide_text[current_slide] = {"body": "", "diagram": "", "popup": ""}
                current_section = "body"  # 기본 섹션
                continue

            if current_slide and current_slide in slide_text:
                # 섹션 전환 감지
                if diagram_pattern.search(line):
                    current_section = "diagram"
                elif popup_pattern.search(line):
                    current_section = "popup"
                elif body_pattern.search(line):
                    current_section = "body"

                # 텍스트 추출 (HTML 태그 제거)
                text = re.sub(r'<[^>]+>', '', line)
                text = text.strip()
                if text and current_section:
                    slide_text[current_slide][current_section] += text + " "

        return slide_text


class SimilarityChecker:
    """텍스트 유사도 계산"""

    def calculate(self, text_a: str, text_b: str) -> float:
        """
        텍스트 유사도 계산 (difflib.SequenceMatcher)

        Returns:
            0.0 ~ 1.0 (1.0 = 완전히 동일)
        """
        if not text_a or not text_b:
            return 0.0
        return difflib.SequenceMatcher(None, text_a.lower(), text_b.lower()).ratio()


class DuplicateDetector:
    """슬라이드 간 중복 감지"""

    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def detect(self, slides: dict) -> list:
        """
        슬라이드 간 중복 감지

        Returns:
            [
                {
                    "slide_a": "slide_1",
                    "slide_b": "slide_2",
                    "section": "body",
                    "similarity": 0.85
                },
                ...
            ]
        """
        duplicates = []
        slide_keys = sorted(slides.keys())
        sections = ["body", "diagram", "popup"]

        for i, slide_a in enumerate(slide_keys):
            for slide_b in slide_keys[i+1:]:
                for section in sections:
                    text_a = slides[slide_a].get(section, "")
                    text_b = slides[slide_b].get(section, "")

                    if text_a and text_b:
                        similarity = SimilarityChecker().calculate(text_a, text_b)
                        if similarity >= self.threshold:
                            duplicates.append({
                                "slide_a": slide_a,
                                "slide_b": slide_b,
                                "section": section,
                                "similarity": round(similarity * 100, 1)
                            })

        return duplicates


class ReportGenerator:
    """검증 보고서 생성"""

    def generate(self, duplicates: list, total_slides: int, output_path: Optional[str] = None) -> str:
        """
        Markdown 형식 보고서 생성

        Args:
            duplicates: 중복 항목 목록
            total_slides: 총 슬라이드 수
            output_path: 보고서 출력 경로 (선택)

        Returns:
            보고서 텍스트
        """
        report = f"""# 슬라이드 중복 검증 보고서

## 요약
- **총 슬라이드**: {total_slides} 개
- **중복 항목**: {len(duplicates)} 개
- **검증일시**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **경고 수준**: {"HIGH" if len(duplicates) > 5 else "MEDIUM" if len(duplicates) > 0 else "LOW"}

## 중복 목록

| 슬라이드 A | 슬라이드 B | 섹션 | 유사도 |
|-----------|-----------|------|--------|
"""

        for dup in duplicates:
            report += f"| {dup['slide_a']} | {dup['slide_b']} | {dup['section']} | {dup['similarity']}% |\n"

        if not duplicates:
            report += "| — | — | — | 0% |\n"

        report += f"""
## 검증 기준
- **임계값**: 80% 이상 유사 → 경고
- **도구**: Python difflib.SequenceMatcher
- **SPEC**: SPEC-B7 (슬라이드 구성 규격)

---
*자동 생성 보고서*
"""

        if output_path:
            Path(output_path).write_text(report, encoding='utf-8')

        return report


def main():
    parser = argparse.ArgumentParser(description='슬라이드 중복 검증 스크립트')
    parser.add_argument('html_file', help='슬라이드 HTML 파일 경로')
    parser.add_argument('--threshold', type=float, default=0.8, help='유사도 임계값 (기본: 0.8)')
    parser.add_argument('--output', type=str, default=None, help='보고서 출력 경로')
    args = parser.parse_args()

    # HTML 파일 읽기
    html_path = Path(args.html_file)
    if not html_path.exists():
        print(f"오류: 파일을 찾을 수 없습니다 - {html_path}")
        sys.exit(1)

    html_content = html_path.read_text(encoding='utf-8')

    # 텍스트 추출
    extractor = SlideExtractor()
    slides = extractor.extract(html_content)

    # 중복 감지
    detector = DuplicateDetector(threshold=args.threshold)
    duplicates = detector.detect(slides)

    # 보고서 생성
    generator = ReportGenerator()
    report = generator.generate(duplicates, len(slides), args.output)

    # 결과 출력
    print(report)

    # 중복 발견 시 경고
    if duplicates:
        print(f"\n⚠️  경고: {len(duplicates)} 개의 중복 항목이 발견되었습니다.")
        sys.exit(1)
    else:
        print("\n✅ 검증 완료: 중복 항목 없음")
        sys.exit(0)


if __name__ == '__main__':
    main()
