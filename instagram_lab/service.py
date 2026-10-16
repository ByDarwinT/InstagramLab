"""Orquestación compartida por la consola y la interfaz web.

No contiene selectores HTML: se delegan a scraper.py para separar responsabilidades.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from .config import PRIMARY_USER, PRIMARY_PASS, RESULTS_DIR
from .auth import initialize_auth, refresh_auth_if_needed
from .scraper import extract_profile_data, collect_post_urls, extract_post_data
from .utils import random_pause


def normalize_profile(raw: str) -> str:
    """Admite @usuario, usuario o URL; evita navegar a dominios arbitrarios."""
    value = raw.strip().lstrip('@')
    if value.startswith(('https://', 'http://')):
        parsed = urlparse(value)
        if parsed.hostname not in {'instagram.com', 'www.instagram.com'}:
            raise ValueError('La URL debe pertenecer a instagram.com')
        value = parsed.path.strip('/').split('/')[0]
    if not re.fullmatch(r'[A-Za-z0-9._]{1,30}', value):
        raise ValueError('Usuario de Instagram no válido')
    return f'https://www.instagram.com/{value}/'


def run_scrape(target: str, max_posts: int = 2, progress=None) -> Path:
    """Ejecuta una sesión completa y devuelve la ruta del JSON generado."""
    if not PRIMARY_USER or not PRIMARY_PASS:
        raise RuntimeError('Configura INSTAGRAM_USERNAME e INSTAGRAM_PASSWORD en .env')
    url = normalize_profile(target)
    count = int(max_posts)
    if not 1 <= count <= 100:
        raise ValueError('La cantidad debe estar entre 1 y 100')
    emit = progress or (lambda message: print(message))
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        try:
            context = browser.new_context(viewport={'width': 1280, 'height': 800}, locale='es-ES')
            page = context.new_page()
            emit('Iniciando sesión…')
            initialize_auth(page, context)
            emit('Leyendo los datos del perfil…')
            profile = extract_profile_data(page, url)
            emit('Buscando publicaciones…')
            urls = collect_post_urls(page, url, count)
            posts = []
            for index, post_url in enumerate(urls, 1):
                if index % 20 == 0:
                    refresh_auth_if_needed(page, context)
                emit(f'Extrayendo publicación {index} de {len(urls)}…')
                post = extract_post_data(page, post_url, index)
                if post is not None:
                    posts.append(post)
                random_pause()
            username = urlparse(url).path.strip('/')
            stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            destination = RESULTS_DIR / f'{username}_{stamp}.json'
            destination.write_text(json.dumps({'perfil': profile, 'publicaciones': posts}, ensure_ascii=False, indent=2), encoding='utf-8')
            emit(f'Finalizado: {len(posts)} publicaciones guardadas')
            return destination
        finally:
            browser.close()
