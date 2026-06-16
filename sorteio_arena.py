"""
Sorteio Arena Guarás — Gerador (Página de escolha + QR Code)
Versão: v2.0 - 2026-06-16

O QR Code abre uma PÁGINA com dois botões: o usuário escolhe
ir para o Instagram OU para o formulário do sorteio.
(Um QR guarda 1 link só; por isso a escolha mora na página, não no QR.)

>>> SEM SERVIDOR <<<
Este script NÃO sobe servidor. Ele só faz duas coisas:
  1. Gera a página 'index.html' (com seus dois links).
  2. Gera o 'qr_arena.png' apontando para URL_DA_PAGINA.

Para o QR funcionar ao ser escaneado, a página precisa estar
no ar num endereço fixo. Isso NÃO é "ligar um servidor": é
hospedagem estática gratuita, que fica no ar 24/7 sozinha.

PASSO A PASSO:
  1. Publique o 'index.html' (escolha um):
       - Rápido, sem conta:  arraste a pasta em  app.netlify.com/drop
       - Permanente (GitHub): repo público -> Settings -> Pages
  2. Cole a URL pública em URL_DA_PAGINA, abaixo.
  3. Rode o script:  python sorteio_arena.py
     -> 'qr_arena.png' pronto pra imprimir. Funciona em qualquer
        celular, a qualquer hora, sem manter nada ligado.

AMBIENTE (uv):
    uv venv /home/noemia2/Desktop/AMBIENTES_VIRTUAIS/PORTO_VIADO --python 3.14 --seed
    source /home/noemia2/Desktop/AMBIENTES_VIRTUAIS/PORTO_VIADO/bin/activate
    uv pip install "qrcode[pil]"     # Pillow vem junto pelo [pil]; nada alem disso
==================================================================
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

# ==================================================================
# CONFIGURAÇÃO (tudo hardcoded — edite só esta seção)
# ==================================================================

LINK_INSTAGRAM = "https://www.instagram.com/arenaguaras?utm_source=qr&igsh=NnNuYW8xdXdxOXd6"
LINK_FORMULARIO = "https://forms.gle/Yzr2ADU5ExBPPyAd8"

# >>> URL pública da página DEPOIS de publicada. O QR aponta pra cá. <<<
URL_DA_PAGINA = "https://devnoem.github.io/arena-guaras/"

ARQUIVO_HTML = "index.html"
ARQUIVO_QR = "qr_arena.png"

# Cores do QR (escarlate do guará sobre branco = alto contraste, leitura fácil)
COR_FRENTE = (229, 52, 43)
COR_FUNDO = (255, 255, 255)

# ==================================================================
# PÁGINA (HTML) — gerada pelo script. __INSTAGRAM__ e __FORMULARIO__
# são substituídos pelos links acima.
# ==================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Arena Guarás · Sorteio</title>
<meta name="description" content="Concorra a 1 mês de aula grátis para você + 1 acompanhante. Beach Tennis, Futevôlei ou Vôlei.">
<meta property="og:title" content="Sorteio Arena Guarás — 1 mês de aula grátis">
<meta property="og:description" content="Para você + 1 acompanhante. Escolha: Beach Tennis, Futevôlei ou Vôlei.">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --areia:#F7EFE0; --areia-2:#EFE0C5; --creme:#FFFCF5;
    --guara:#E5342B; --guara-fundo:#C3261F;
    --mar:#0C6E6E; --sol:#F4A300;
    --carvao:#241A12; --carvao-suave:#6E5E4E;
  }
  *{ box-sizing:border-box; margin:0; padding:0; }
  html,body{ height:100%; }
  body{
    font-family:"Inter", system-ui, sans-serif; color:var(--carvao);
    background:radial-gradient(120% 90% at 50% -10%, #FFF6E2 0%, var(--areia) 45%, var(--areia-2) 100%);
    min-height:100%; display:flex; align-items:center; justify-content:center;
    padding:24px 18px calc(24px + env(safe-area-inset-bottom));
    overflow-x:hidden; -webkit-font-smoothing:antialiased;
  }
  .palco{ position:relative; width:100%; max-width:430px; }
  .palco::before{
    content:""; position:absolute; top:-90px; left:50%;
    width:560px; height:560px; transform:translateX(-50%);
    background:repeating-conic-gradient(from 0deg at 50% 50%,
      rgba(244,163,0,.16) 0deg 9deg, transparent 9deg 18deg);
    border-radius:50%;
    -webkit-mask:radial-gradient(circle, #000 0%, #000 30%, transparent 62%);
            mask:radial-gradient(circle, #000 0%, #000 30%, transparent 62%);
    animation:girar 90s linear infinite; z-index:0; pointer-events:none;
  }
  @keyframes girar{ to{ transform:translateX(-50%) rotate(360deg); } }
  .bilhete{
    position:relative; z-index:1; background:var(--creme);
    border-radius:26px; padding:30px 26px 26px;
    box-shadow:0 1px 0 rgba(255,255,255,.9) inset,
      0 30px 60px -24px rgba(36,26,18,.45), 0 8px 22px -12px rgba(36,26,18,.3);
    animation:entrar .7s cubic-bezier(.2,.7,.2,1) both;
  }
  .bilhete::before,.bilhete::after{
    content:""; position:absolute; top:50%; width:30px; height:30px;
    background:var(--areia); border-radius:50%; transform:translateY(-50%);
    box-shadow:0 0 0 1px rgba(36,26,18,.05) inset;
  }
  .bilhete::before{ left:-15px; }
  .bilhete::after{ right:-15px; }
  @keyframes entrar{ from{ opacity:0; transform:translateY(22px) scale(.97); } to{ opacity:1; transform:none; } }
  .topo{ display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
  .marca{ display:inline-flex; align-items:center; gap:7px; font-weight:800; font-size:13px;
    letter-spacing:.14em; text-transform:uppercase; color:var(--carvao); }
  .marca .bolinha{ width:9px; height:9px; border-radius:50%; background:var(--guara);
    box-shadow:0 0 0 4px rgba(229,52,43,.18); }
  .selo{ font-weight:800; font-size:11px; letter-spacing:.18em; text-transform:uppercase;
    color:var(--mar); background:rgba(12,110,110,.1); padding:6px 11px; border-radius:999px; }
  .chamada{ font-size:14px; font-weight:600; color:var(--carvao-suave); letter-spacing:.02em; margin-bottom:4px; }
  h1{ font-family:"Anton", sans-serif; font-weight:400; font-size:clamp(46px, 16vw, 64px);
    line-height:.92; letter-spacing:.01em; text-transform:uppercase; color:var(--guara); margin:2px 0 14px; }
  h1 .destaque{ color:var(--carvao); }
  .acompanhante{ font-size:16px; color:var(--carvao); margin-bottom:18px; }
  .acompanhante strong{ color:var(--guara); font-weight:800; }
  .modalidades{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:24px; }
  .modalidades span{ font-size:13px; font-weight:700; color:var(--mar); background:#fff;
    border:1.5px solid rgba(12,110,110,.25); padding:8px 13px; border-radius:999px; }
  .picote{ border:none; border-top:2px dashed rgba(36,26,18,.18); margin:4px 0 22px; }
  .acoes{ display:flex; flex-direction:column; gap:12px; }
  .btn{ display:flex; align-items:center; justify-content:center; gap:9px; min-height:60px;
    padding:0 20px; border-radius:16px; font-size:17px; font-weight:800; text-decoration:none;
    letter-spacing:.01em; transition:transform .12s ease, box-shadow .2s ease, background .2s ease;
    -webkit-tap-highlight-color:transparent; }
  .btn:active{ transform:translateY(2px) scale(.99); }
  .btn-guara{ background:var(--guara); color:#fff; box-shadow:0 12px 22px -10px rgba(229,52,43,.7); }
  .btn-guara:hover{ background:var(--guara-fundo); }
  .btn-mar{ background:#fff; color:var(--mar); border:2px solid var(--mar); }
  .btn-mar:hover{ background:var(--mar); color:#fff; }
  .btn-mar:hover .ig path{ fill:#fff; }
  .btn .seta{ font-size:20px; }
  .nota{ font-size:12px; line-height:1.45; color:var(--carvao-suave); text-align:center; margin-top:18px; }
  .btn:focus-visible{ outline:3px solid var(--sol); outline-offset:3px; }
  @media (prefers-reduced-motion: reduce){
    .palco::before{ animation:none; } .bilhete{ animation:none; } .btn{ transition:none; }
  }
</style>
</head>
<body>
  <div class="palco">
    <main class="bilhete">
      <div class="topo">
        <span class="marca"><span class="bolinha"></span> Arena Guarás</span>
        <span class="selo">Sorteio</span>
      </div>
      <p class="chamada">Você está concorrendo a</p>
      <h1>1 Mês<br>de aula <span class="destaque">grátis</span></h1>
      <p class="acompanhante">para você <strong>+ 1 acompanhante</strong></p>
      <div class="modalidades">
        <span>Beach Tennis</span><span>Futevôlei</span><span>Vôlei</span>
      </div>
      <hr class="picote">
      <div class="acoes">
        <a class="btn btn-guara" href="__FORMULARIO__">
          Quero concorrer <span class="seta">&rarr;</span>
        </a>
        <a class="btn btn-mar" href="__INSTAGRAM__">
          <svg class="ig" width="22" height="22" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="#0C6E6E" d="M12 2.2c3.2 0 3.6 0 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s0 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58 0-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.21 15.58 2.2 15.2 2.2 12s0-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.21 8.8 2.2 12 2.2Zm0 1.62c-3.15 0-3.52.01-4.76.07-.9.04-1.39.19-1.71.32-.43.17-.74.37-1.06.69-.32.32-.52.63-.69 1.06-.13.32-.28.81-.32 1.71-.06 1.24-.07 1.61-.07 4.76s0 3.52.07 4.76c.04.9.19 1.39.32 1.71.17.43.37.74.69 1.06.32.32.63.52 1.06.69.32.13.81.28 1.71.32 1.24.06 1.61.07 4.76.07s3.52 0 4.76-.07c.9-.04 1.39-.19 1.71-.32.43-.17.74-.37 1.06-.69.32-.32.52-.63.69-1.06.13-.32.28-.81.32-1.71.06-1.24.07-1.61.07-4.76s0-3.52-.07-4.76c-.04-.9-.19-1.39-.32-1.71a2.85 2.85 0 0 0-.69-1.06 2.85 2.85 0 0 0-1.06-.69c-.32-.13-.81-.28-1.71-.32-1.24-.06-1.61-.07-4.76-.07Zm0 2.76a5.42 5.42 0 1 1 0 10.84 5.42 5.42 0 0 1 0-10.84Zm0 1.62a3.8 3.8 0 1 0 0 7.6 3.8 3.8 0 0 0 0-7.6Zm5.6-2.9a1.27 1.27 0 1 1 0 2.54 1.27 1.27 0 0 1 0-2.54Z"/>
          </svg>
          Seguir no Instagram
        </a>
      </div>
      <p class="nota">*1 mês de aula gratuita na modalidade escolhida. Sujeito ao regulamento da promoção.</p>
    </main>
  </div>
</body>
</html>
"""


# ==================================================================
# FUNÇÕES
# ==================================================================

def gerar_html():
    """Grava index.html com os dois links injetados."""
    pagina = HTML_TEMPLATE.replace("__INSTAGRAM__", LINK_INSTAGRAM)
    pagina = pagina.replace("__FORMULARIO__", LINK_FORMULARIO)
    with open(ARQUIVO_HTML, "w", encoding="utf-8") as arq:
        arq.write(pagina)
    print(f"[OK] Pagina gerada: {ARQUIVO_HTML}")


def gerar_qr(url):
    """Gera o QR Code estilizado (escarlate, cantos arredondados) apontando para 'url'."""
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # H = aguenta logo no centro
        box_size=20,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(front_color=COR_FRENTE, back_color=COR_FUNDO),
    )
    img.save(ARQUIVO_QR)
    print(f"[OK] QR Code gerado: {ARQUIVO_QR}  ->  {url}")


def main():
    print("=== Sorteio Arena Guaras — gerador de pagina + QR ===\n")
    gerar_html()
    gerar_qr(URL_DA_PAGINA)
    print("\n--- PRONTO ---")
    print(f"O QR aponta para: {URL_DA_PAGINA}")
    print("Publique o index.html nesse endereco (Netlify Drop ou GitHub Pages)")
    print("antes de imprimir. Sem pagina no ar, o QR abre pagina inexistente.")


if __name__ == "__main__":
    main()
