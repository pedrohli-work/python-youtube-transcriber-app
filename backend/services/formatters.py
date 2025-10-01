import re

def join_sentences(lines: list[str]) -> str:
    return "\n".join([ln.strip() for ln in lines if ln and ln.strip()]).strip()

def vtt_to_lines(vtt_text: str) -> list[str]:
    lines, buf = [], []
    for ln in vtt_text.splitlines():
        s = ln.strip()
        if not s:
            if buf:
                text = " ".join(buf).strip()
                if text: lines.append(text)
                buf=[]
            continue
        if s.startswith("WEBVTT") or re.match(r"^\d+$", s) or re.search(r"-->", s):
            continue
        buf.append(s)
    if buf:
        text = " ".join(buf).strip()
        if text: lines.append(text)
    return lines

def srt_to_lines(srt_text: str) -> list[str]:
    lines, buf = [], []
    for ln in srt_text.splitlines():
        s = ln.strip()
        if not s:
            if buf:
                lines.append(" ".join(buf).strip()); buf=[]
            continue
        if re.match(r"^\d+$", s) or re.search(r"-->", s):
            continue
        buf.append(s)
    if buf: lines.append(" ".join(buf).strip())
    return lines

def to_srt_from_segments(segments) -> str:
    def ts(t):
        h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int((t-int(t))*1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    out=[]
    for i,s in enumerate(segments,1):
        txt = (s.text or "").strip()
        if not txt: continue
        out.append(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{txt}\n")
    return "\n".join(out)

def to_vtt_from_segments(segments) -> str:
    def ts(t):
        h=int(t//3600); m=int((t%3600)//60); s=t%60
        return f"{h:02d}:{m:02d}:{s:06.3f}"  # ponto como separador decimal
    out=["WEBVTT\n"]
    for s in segments:
        txt = (s.text or "").strip()
        if not txt: continue
        out.append(f"{ts(s.start)} --> {ts(s.end)}\n{txt}\n")
    return "\n".join(out)
