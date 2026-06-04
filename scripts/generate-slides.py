#!/usr/bin/env python3
"""
슬라이드 코드 생성 스크립트

SPEC-B7 기준:
- specs/content/*.md 파일 읽기
- Jinja2 템플릿 적용
- docs/slides.html 생성

사용법:
    python scripts/generate-slides.py
"""

import argparse
import glob
import os
import sys
from pathlib import Path
from datetime import datetime

import yaml


def load_spec_file(filepath: str) -> dict:
    """Spec 파일 읽기"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # YAML frontmatter 추출
    parts = content.split('---')
    if len(parts) < 3:
        return {}
    
    metadata = yaml.safe_load(parts[1])
    body = parts[2]
    
    # 섹션 분리
    sections = {}
    current_section = None
    current_content = []
    
    for line in body.split('\n'):
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    metadata['sections'] = sections
    return metadata


def generate_html(specs: list, template_path: str, output_path: str):
    """HTML 생성"""
    # 간단한 템플릿 처리 (Jinja2 없이)
    html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>에이전트 메모리 시스템</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #ffffff;
        }
        .slide {
            display: none;
            max-width: 1200px;
            padding: 40px;
        }
        .slide.active {
            display: block;
        }
        h1 { font-size: 56px; }
        h2 { font-size: 44px; }
        p { font-size: 16px; line-height: 1.7; }
    </style>
</head>
<body>
"""
    for spec in specs:
        html += f"""
<div class="slide" data-slide="{spec.get('slide_number', 0)}">
    <span class="label">{spec.get('label', '')}</span>
    <h1>{spec.get('title', '')}</h1>
    <div class="body">
        {spec.get('sections', {}).get('본문', '')}
    </div>
</div>
"""
    
    html += """
<script>
    // 슬라이드 네비게이션
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    
    function showSlide(n) {
        slides.forEach(s => s.classList.remove('active'));
        slides[n].classList.add('active');
    }
    
    // 키보드 네비게이션
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            currentSlide = Math.min(currentSlide + 1, slides.length - 1);
            showSlide(currentSlide);
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            currentSlide = Math.max(currentSlide - 1, 0);
            showSlide(currentSlide);
        }
    });
    
    // 초기화
    showSlide(0);
</script>
</body>
</html>
"""
    
    Path(output_path).write_text(html, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='슬라이드 코드 생성 스크립트')
    parser.add_argument('--spec-dir', type=str, default='specs/content', help='Spec 파일 디렉토리')
    parser.add_argument('--output', type=str, default='docs/slides.html', help='출력 파일 경로')
    args = parser.parse_args()
    
    # Spec 파일 읽기
    spec_files = sorted(glob.glob(os.path.join(args.spec_dir, '*.md')))
    if not spec_files:
        print(f"오류: Spec 파일을 찾을 수 없습니다 - {args.spec_dir}")
        sys.exit(1)
    
    specs = []
    for filepath in spec_files:
        spec = load_spec_file(filepath)
        if spec:
            specs.append(spec)
    
    # HTML 생성
    generate_html(specs, None, args.output)
    
    print(f"✅ {len(specs)} 개 슬라이드 생성 완료: {args.output}")


if __name__ == '__main__':
    main()
