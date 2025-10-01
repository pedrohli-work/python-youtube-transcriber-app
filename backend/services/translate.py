def to_ptbr(lines):
    try:
        import argostranslate.package, argostranslate.translate
        installed = argostranslate.translate.get_installed_languages()
        code_map = {l.code: l for l in installed}
        en, pt = code_map.get("en"), code_map.get("pt")
        if not (en and pt):
            return lines
        translator = en.get_translation(pt)
        return [translator.translate(t) for t in lines]
    except Exception:
        return lines
