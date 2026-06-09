#!/usr/bin/env python3
import argparse
import glob
import os
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import yaml

def load_spec_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---')
    if len(parts) < 3: return {}
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

def update_index_metadata(specs, output_path):
    docs_dir = os.path.dirname(output_path)
    project_dir = os.path.dirname(docs_dir)
    index_path = os.path.join(project_dir, 'specs', '_index.yaml')
    if not os.path.exists(index_path): return
    tz_kr = timezone(timedelta(hours=9))
    now = datetime.now(tz_kr)
    with open(index_path, 'r', encoding='utf-8') as f: content = f.read()
    content = re.sub(r'^updated:.*$', f"updated: '{now.strftime('%Y-%m-%d')}'", content, flags=re.MULTILINE)
    if 'last_built_at:' in content:
        content = re.sub(r'^last_built_at:.*$', f"last_built_at: '{now.isoformat()}'", content, flags=re.MULTILINE)
    else:
        content = content.replace("updated: ", f"updated: \nlast_built_at: '{now.isoformat()}'\n")
    if 'last_built_version:' in content:
        content = re.sub(r'^last_built_version:.*$', "last_built_version: v1.8", content, flags=re.MULTILINE)
    else:
        content = content.replace("last_built_at:", f"last_built_version: v1.8\nlast_built_at:")
    with open(index_path, 'w', encoding='utf-8') as f: f.write(content)

def generate_html(specs, output_path):
    css = """
    :root { --bg: #ffffff; --bg-card: #f9fafb; --border: #e5e7eb; --text: #1a1a1a; --text-dim: #666666; --text-bright: #000000; --accent: #2563eb; --accent-dim: rgba(37,99,235,0.1); }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: var(--bg); color: var(--text); font-family: 'Noto Sans KR', sans-serif; overflow: hidden; height: 100vh; width: 100vw; }
    .slides { width: 100vw; height: 100vh; position: relative; }
    .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 80px 100px; opacity: 0; transform: translateY(20px); transition: all 0.5s ease; pointer-events: none; }
    .slide.active { opacity: 1; transform: translateY(0); pointer-events: all; }
    .slide-label { font-size: 13px; font-weight: 600; color: var(--accent); margin-bottom: 24px; text-transform: uppercase; }
    h1 { font-size: 56px; font-weight: 900; color: var(--text-bright); text-align: center; }
    h2 { font-size: 44px; font-weight: 800; color: var(--text-bright); text-align: center; margin-bottom: 32px; }
    p { font-size: 16px; color: var(--text-dim); line-height: 1.7; text-align: center; white-space: pre-wrap; }
    .popup-trigger { display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 50%; background: var(--accent-dim); color: var(--accent); font-size: 11px; font-weight: 700; cursor: pointer; margin-left: 4px; vertical-align: middle; transition: all 0.2s; }
    .popup-trigger:hover { background: var(--accent); color: white; transform: scale(1.1); }
    .popup-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 200; display: none; justify-content: center; align-items: center; padding: 40px; backdrop-filter: blur(4px); }
    .popup-overlay.active { display: flex; }
    .popup-content { background: var(--bg); border: 1px solid var(--border); border-radius: 16px; padding: 36px; max-width: 600px; max-height: 70vh; overflow-y: auto; position: relative; text-align: left; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
    .popup-close { position: absolute; top: 20px; right: 20px; background: none; border: none; font-size: 24px; cursor: pointer; }
    .popup-content h4 { font-size: 20px; margin-bottom: 16px; color: var(--accent); border-bottom: 2px solid var(--accent-dim); padding-bottom: 8px; }
    .nav { position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 16px; z-index: 100; background: rgba(255,255,255,0.95); border: 1px solid var(--border); border-radius: 100px; padding: 10px 24px; }
    .nav button { background: none; border: none; color: var(--text-dim); cursor: pointer; font-size: 20px; width: 36px; height: 36px; border-radius: 50%; }
    .nav-counter { font-family: monospace; font-size: 14px; color: var(--text-dim); min-width: 60px; text-align: center; }
    .nav-dots { display: flex; gap: 4px; }
    .nav-dot { width: 6px; height: 6px; border-radius: 3px; background: var(--border); cursor: pointer; transition: all 0.3s; }
    .nav-dot.active { background: var(--accent); width: 20px; }
    """
    
    js = """
    const pData = POPUP_PLACEHOLDER;
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
        const content = pData[key] || '내용 없음';
        document.getElementById('popupBody').innerHTML = `<h4>${key.split('_').slice(1).join(' ').toUpperCase()}</h4><p>${content}</p>`;
        document.getElementById('popupOverlay').classList.add('active');
    }
    function hidePopup() { document.getElementById('popupOverlay').classList.remove('active'); }
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); nextSlide(); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); prevSlide(); }
        if (e.key === 'Escape') { hidePopup(); }
    });
    goTo(0);
    """
    
    popup_data = {}
    html_slides = []
    
    for spec in specs:
        s_num = spec.get('slide_number', 0)
        label = spec.get('label', '')
        title = spec.get('title', '')
        body = spec.get('sections', {}).get('본문', '')
        popup_raw = spec.get('sections', {}).get('팝업', '')
        
        slide_popup_map = {}
        if popup_raw:
            for line in popup_raw.split('\n'):
                if line.strip().startswith('- **'):
                    match = re.match(r'^- \*\*(.*?)\*\*:\s*(.*)', line.strip())
                    if match:
                        kw, desc = match.groups()
                        key = f"s{s_num}_{kw.replace(' ', '_').lower()}"
                        slide_popup_map[kw] = {'key': key, 'desc': desc}
                        popup_data[key] = desc
        
        processed_body = body
        if slide_popup_map:
            sorted_kws = sorted(slide_popup_map.keys(), key=len, reverse=True)
            for kw in sorted_kws:
                if kw in processed_body:
                    trigger = f'<span class="popup-trigger" onclick="showPopup(\'{slide_popup_map[kw]["key"]}\')">?</span>'
                    processed_body = processed_body.replace(kw, f'{kw}{trigger}', 1)
        
        slide_html = f'<div class="slide" data-slide="{s_num}"><div class="slide-label">{label}</div>'
        if s_num == 1:
            slide_html += f'<div class="slide-cover"><h1>{title}</h1><p class="subtitle">{spec.get("subtitle", "")}<br>{spec.get("description", "")}</p></div>'
        else:
            slide_html += f'<h2>{title}</h2>'
            if processed_body: slide_html += f'<p>{processed_body}</p>'
        slide_html += '</div>'
        html_slides.append(slide_html)
        
    final_js = js.replace('POPUP_PLACEHOLDER', json.dumps(popup_data, ensure_ascii=False))
    
    full_html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><title>AI 에게 기억을 선물하다</title><style>{css}</style></head><body>
    <div class="slides" id="slides">
    {''.join(html_slides)}
    </div>
    <div class="popup-overlay" id="popupOverlay" onclick="hidePopup()"><div class="popup-content" id="popupContent" onclick="event.stopPropagation()"><button class="popup-close" onclick="hidePopup()">×</button><div id="popupBody"></div></div></div>
    <div class="nav"><button onclick="prevSlide()">‹</button><div class="nav-dots" id="navDots"></div><span class="nav-counter" id="navCounter">1 / 11</span><button onclick="nextSlide()">›</button></div>
    <script>{final_js}</script>
    </body></html>"""
    
    Path(output_path).write_text(full_html, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec-dir', type=str, default='specs/content')
    parser.add_argument('--output', type=str, default='docs/slides.html')
    args = parser.parse_args()
    spec_files = sorted(glob.glob(os.path.join(args.spec_dir, '*.md')))
    specs = [load_spec_file(f) for f in spec_files if load_spec_file(f)]
    generate_html(specs, args.output)
    update_index_metadata(specs, args.output)

if __name__ == '__main__':
    main()
