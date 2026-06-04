#!/usr/bin/env python3
"""
슬라이드 코드 생성 스크립트 (v2.0)

SPEC-B7 기준:
- specs/content/*.md 파일 읽기
- 본문/다이어그램/팝업 분리 렌더링
- 팝업 데이터 JS 객체 자동 생성
- docs/slides.html 생성
"""

import argparse
import glob
import os
import sys
from pathlib import Path
import yaml

def load_spec_file(filepath: str) -> dict:
    """Spec 파일 읽기"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---')
    if len(parts) < 3:
        return {}
    
    metadata = yaml.safe_load(parts[1])
    body_text = parts[2]
    
    sections = {}
    current_section = None
    current_content = []
    
    for line in body_text.split('\n'):
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

def generate_html(specs: list, output_path: str):
    """HTML 생성"""
    # 템플릿 시작
    html = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 에게 기억을 선물하다 | 파일 기반 지식 시스템</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
  :root {
    --bg: #ffffff; --bg-card: #f9fafb; --bg-card-hover: #f3f4f6; --border: #e5e7eb;
    --text: #1a1a1a; --text-dim: #666666; --text-bright: #000000;
    --accent: #2563eb; --accent-dim: rgba(37,99,235,0.1);
    --green: #059669; --green-dim: rgba(5,150,105,0.1);
    --purple: #7c3aed; --purple-dim: rgba(124,58,237,0.1);
    --amber: #d97706; --amber-dim: rgba(217,119,6,0.1);
    --rose: #e11d48; --rose-dim: rgba(225,29,72,0.1);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--text); font-family: 'Noto Sans KR', 'Inter', sans-serif; overflow: hidden; height: 100vh; width: 100vw; }
  .slides { width: 100vw; height: 100vh; position: relative; }
  .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 80px 100px; opacity: 0; transform: translateY(20px); transition: opacity 0.5s ease, transform 0.5s ease; pointer-events: none; overflow: hidden; }
  .slide.active { opacity: 1; transform: translateY(0); pointer-events: all; }
  .slide-label { font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 24px; opacity: 0.8; }
  h1 { font-size: 56px; font-weight: 900; line-height: 1.15; color: var(--text-bright); margin-bottom: 16px; text-align: center; }
  h2 { font-size: 44px; font-weight: 800; line-height: 1.2; color: var(--text-bright); margin-bottom: 32px; text-align: center; }
  p, .subtitle { font-size: 16px; color: var(--text-dim); line-height: 1.7; text-align: center; }
  .slide-cover h1 { color: var(--accent); font-size: 64px; }
  .cover-meta { margin-top: 40px; display: flex; gap: 40px; font-size: 16px; color: var(--text-dim); }
  .cover-meta span { display: flex; align-items: center; gap: 10px; }
  .cover-meta .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }
  .content-grid { display: grid; gap: 20px; margin-top: 16px; width: 100%; max-width: 1200px; }
  .grid-3 { grid-template-columns: 1fr 1fr 1fr; }
  .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 28px; text-align: center; }
  .diagram { display: flex; align-items: center; gap: 12px; margin: 24px 0; flex-wrap: wrap; justify-content: center; }
  .diagram-node { background: var(--bg-card); border: 2px solid var(--border); border-radius: 12px; padding: 16px 24px; text-align: center; font-size: 16px; font-weight: 600; }
  .diagram-node.accent { border-color: var(--accent); background: var(--accent-dim); color: var(--accent); }
  .diagram-node.green { border-color: var(--green); background: var(--green-dim); color: var(--green); }
  .diagram-node.purple { border-color: var(--purple); background: var(--purple-dim); color: var(--purple); }
  .diagram-arrow { font-size: 24px; color: var(--text-dim); opacity: 0.5; }
  .diagram-label { font-size: 12px; color: var(--text-dim); margin-top: 4px; }
  .popup-trigger { display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 50%; background: var(--accent-dim); color: var(--accent); font-size: 12px; font-weight: 700; cursor: pointer; margin-left: 6px; vertical-align: middle; }
  .popup-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 200; display: none; justify-content: center; align-items: center; padding: 40px; }
  .popup-overlay.active { display: flex; }
  .popup-content { background: var(--bg); border: 1px solid var(--border); border-radius: 16px; padding: 36px; max-width: 900px; max-height: 80vh; overflow-y: auto; position: relative; text-align: left; }
  .popup-close { position: absolute; top: 20px; right: 20px; background: none; border: none; color: var(--text-dim); font-size: 24px; cursor: pointer; }
  .popup-content h4 { font-size: 18px; margin-bottom: 12px; color: var(--accent); }
  .popup-content p { text-align: left; margin-bottom: 14px; }
  .nav { position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 16px; z-index: 100; background: rgba(255,255,255,0.95); backdrop-filter: blur(16px); border: 1px solid var(--border); border-radius: 100px; padding: 10px 24px; }
  .nav button { background: none; border: none; color: var(--text-dim); cursor: pointer; font-size: 20px; width: 36px; height: 36px; border-radius: 50%; }
  .nav-counter { font-family: 'Inter', monospace; font-size: 14px; color: var(--text-dim); min-width: 60px; text-align: center; }
  .nav-dots { display: flex; gap: 4px; }
  .nav-dot { width: 6px; height: 6px; border-radius: 3px; background: var(--border); cursor: pointer; }
  .nav-dot.active { background: var(--accent); width: 20px; }
</style>
</head>
<body>
<div class="slides" id="slides">
"""
    popup_data = {}
    
    for spec in specs:
        s_num = spec.get('slide_number', 0)
        label = spec.get('label', '')
        title = spec.get('title', '')
        body = spec.get('sections', {}).get('본문', '')
        diagram = spec.get('sections', {}).get('다이어그램', '')
        popup = spec.get('sections', {}).get('팝업', '')
        
        # 팝업 데이터 수집 (ID는 label 기반)
        popup_id = label.replace(' ', '_').lower()
        popup_data[popup_id] = popup

        # HTML 슬라이드 생성
        html += f'<div class="slide" data-slide="{s_num}">'
        html += f'<div class="slide-label">{label}</div>'
        
        if s_num == 1:
            html += f'<div class="slide-cover"><h1>{title}</h1>'
            html += f'<p class="subtitle">{spec.get("subtitle", "")}<br>{spec.get("description", "")}</p>'
            html += f'<div class="cover-meta"><span><span class="dot"></span>{spec.get("meta", {}).get("date", "")}</span><span><span class="dot"></span>{spec.get("meta", {}).get("presenter", "")}</span></div></div>'
        else:
            html += f'<h2>{title}'
            if spec.get('popup_trigger', False):
                html += f'<span class="popup-trigger" onclick="showPopup(\'{popup_id}\')">?</span>'
            html += '</h2>'
            
            if body:
                html += f'<p>{body}</p>'
            
            if diagram and diagram != '(없음)':
                html += '<div class="diagram">'
                # 간단한 화살표 처리 및 노드 생성
                nodes = diagram.split('→')
                for i, node in enumerate(nodes):
                    node_text = node.strip()
                    # 색상 지정 로직 (단순화)
                    color_class = "accent" if "구조화" in node_text or "Detail" in node_text else "green" if "정리" in node_text or "Scan" in node_text else "purple"
                    html += f'<div class="diagram-node {color_class}">{node_text}</div>'
                    if i < len(nodes) - 1:
                        html += '<div class="diagram-arrow">→</div>'
                html += '</div>'

        html += '</div>'

    html += """
</div>
<div class="popup-overlay" id="popupOverlay" onclick="hidePopup()">
  <div class="popup-content" id="popupContent" onclick="event.stopPropagation()">
    <button class="popup-close" onclick="hidePopup()">×</button>
    <div id="popupBody"></div>
  </div>
</div>
<div class="nav">
  <button onclick="prevSlide()">‹</button>
  <div class="nav-dots" id="navDots"></div>
  <span class="nav-counter" id="navCounter">1 / 11</span>
  <button onclick="nextSlide()">›</button>
</div>
<script>
  const popupData = """ + str(popup_data) + """
  // 팝업 데이터 처리 (Python dict -> JS object)
  const pData = {
"""
    for k, v in popup_data.items():
        html += f'    "{k}": `{v}`,\n'
    
    html += """  };

  let current = 0;
  const slides = document.querySelectorAll('.slide');
  const total = slides.length;
  const dotsContainer = document.getElementById('navDots');
  const counter = document.getElementById('navCounter');

  for (let i = 0; i < total; i++) {
    const dot = document.createElement('div');
    dot.className = 'nav-dot' + (i === 0 ? ' active' : '');
    dot.onclick = () => goTo(i);
    dotsContainer.appendChild(dot);
  }

  function goTo(n) {
    slides[current].classList.remove('active');
    dotsContainer.children[current].classList.remove('active');
    current = ((n % total) + total) % total;
    slides[current].classList.add('active');
    dotsContainer.children[current].classList.add('active');
    counter.textContent = `${current + 1} / ${total}`;
  }

  function nextSlide() { goTo(current + 1); }
  function prevSlide() { goTo(current - 1); }
  function showPopup(key) {
    document.getElementById('popupBody').innerHTML = pData[key] || '내용 없음';
    document.getElementById('popupOverlay').classList.add('active');
  }
  function hidePopup() { document.getElementById('popupOverlay').classList.remove('active'); }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); nextSlide(); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); prevSlide(); }
    if (e.key === 'Escape') { hidePopup(); }
  });

  goTo(0);
</script>
</body>
</html>
"""
    Path(output_path).write_text(html, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec-dir', type=str, default='specs/content')
    parser.add_argument('--output', type=str, default='docs/slides.html')
    args = parser.parse_args()
    
    spec_files = sorted(glob.glob(os.path.join(args.spec_dir, '*.md')))
    specs = [load_spec_file(f) for f in spec_files if load_spec_file(f)]
    
    generate_html(specs, args.output)
    print(f"✅ {len(specs)} 개 슬라이드 생성 완료: {args.output}")

if __name__ == '__main__':
    main()
