"""
Mini Brownies - Site de Vendas
Flask + HTML + CSS
"""

import json
import os
import time
import urllib.parse
import unicodedata
from functools import wraps

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "brownies-admin-secret-key"

PASTA_UPLOADS = os.path.join(app.root_path, "static", "imagens")

app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

EXTENSOES_PERMITIDAS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
}

os.makedirs(PASTA_UPLOADS, exist_ok=True)


# ============================================================
# CONFIGURAÇÕES
# ============================================================

NOME_DA_MARCA = "Mimi Brownies"

SENHA_ADMIN = os.environ.get(
    "SENHA_ADMIN",
    "brownies2024"
)

ENDERECO_LOJA = (
    "Rua deputado José Francisco de Melo Cavalcante, n° 435 - "
    "Nova Morada, Recife / PE"
)

TEMPO_MEDIO_DELIVERY = "45 - 65 minutos"
TEMPO_MEDIO_BALCAO = "15 - 35 minutos"

RECOMPENSAS_FIDELIDADE = [
    {
        "pontos": 10,
        "premio": "Brownie Tradicional"
    }
]

HORARIOS_FUNCIONAMENTO = [
    {
        "dia": "Domingo",
        "periodos": ["Fechado"]
    },
    {
        "dia": "Segunda",
        "periodos": ["13:30 - 20:30"]
    },
    {
        "dia": "Terça",
        "periodos": [
            "13:30 - 21:30",
            "14:00 - 20:57"
        ]
    },
    {
        "dia": "Quarta",
        "periodos": [
            "13:30 - 21:28",
            "14:00 - 20:57"
        ]
    },
    {
        "dia": "Quinta",
        "periodos": [
            "13:30 - 21:30",
            "14:00 - 20:57"
        ]
    },
    {
        "dia": "Sexta",
        "periodos": [
            "13:30 - 21:30",
            "14:00 - 20:57"
        ]
    },
    {
        "dia": "Sábado",
        "periodos": [
            "13:30 - 21:30",
            "14:00 - 22:57"
        ]
    },
]

METODOS_PAGAMENTO = [
    "Dinheiro",
    "PIX (chave exibida após o envio)",
    "Cartão de Crédito Online",
    "Cartão de Débito - Maquininha",
    "Cartão de Crédito - Maquininha",
    "PicPay",
]

TAXAS_ENTREGA = [
    {"bairro": "Alto do Mandu", "valor": 10.00},
    {"bairro": "Bairro dos Estados", "valor": 7.00},
    {"bairro": "Cdu", "valor": 6.00},
    {"bairro": "Centro Camaragibe", "valor": 7.00},
    {"bairro": "Cidade Universitária", "valor": 6.00},
    {"bairro": "Condomínio Marcos Freire", "valor": 6.00},
    {"bairro": "Dois Irmãos", "valor": 6.00},
    {"bairro": "Engenho do Meio", "valor": 8.00},
    {"bairro": "Engenho Poeta", "valor": 4.00},
    {"bairro": "Graças", "valor": 11.00},
    {"bairro": "IPUTINGA", "valor": 6.00},
    {"bairro": "Iquine", "valor": 0.00},
    {"bairro": "Jardim Primavera", "valor": 6.00},
    {"bairro": "My connect", "valor": 0.00},
    {"bairro": "Nova Morada", "valor": 2.00},
    {"bairro": "Novo Caxangá", "valor": 4.00},
    {"bairro": "Sítio dos Pintos", "valor": 5.00},
    {"bairro": "Torre", "valor": 11.00},
    {"bairro": "UFPE", "valor": 6.00},
    {"bairro": "UFRPE", "valor": 5.00},
    {"bairro": "Ur7", "valor": 6.00},
    {"bairro": "Várzea", "valor": 5.00},
]

WHATSAPP = "5581988300646"

INSTAGRAM_USUARIO = "brownies.mimi"

INSTAGRAM_LINK = (
    f"https://instagram.com/{INSTAGRAM_USUARIO}"
)

CIDADE_REGIAO = "Recife - PE e região"

INFO_ENTREGA = (
    "Entregamos em Recife e região metropolitana. "
    "Retirada disponível mediante combinação prévia."
)

HERO_TITULO = "Mini Brownies feitos com carinho"

HERO_TEXTO = (
    "Brownies artesanais, feitos em pequenos lotes com ingredientes "
    "cuidadosamente selecionados. Perfeitos para presentes, eventos "
    "ou para aquele momento em que bate a vontade de um doce."
)

SOBRE_TITULO = "Feitos com carinho"

SOBRE_TEXTO = (
    "Cada brownie é preparado à mão, com tempo e atenção em cada etapa. "
    "Usamos chocolate de boa qualidade, manteiga real e ingredientes frescos. "
    "Trabalhamos em pequenos lotes para garantir que cada peça saia do forno "
    "no ponto certo — macia por dentro, com aquela casquinha leve por fora. "
    "É uma confeitaria pequena, feita com cuidado de quem ama o que faz."
)


# ============================================================
# ARQUIVOS
# ============================================================

ARQUIVO_PRODUTOS = os.path.join(
    app.root_path,
    "produtos.json"
)

ARQUIVO_CATEGORIAS = os.path.join(
    app.root_path,
    "categorias.json"
)


# ============================================================
# CATEGORIAS INICIAIS
# ============================================================

CATEGORIAS_INICIAIS = [
    {
        "slug": "doces",
        "titulo": "Doces",
        "descricao": (
            "Aqui você encontra nossas opções doces "
            "que não levam brownies"
        ),
    },
    {
        "slug": "brownies-recheados",
        "titulo": "Brownies Recheados",
        "descricao": "",
    },
    {
        "slug": "copo-da-felicidade",
        "titulo": "Copo Da Felicidade",
        "descricao": "",
    },
    {
        "slug": "tradicional",
        "titulo": "Tradicional",
        "descricao": "",
    },
    {
        "slug": "casquinha",
        "titulo": "Casquinha",
        "descricao": "",
    },
    {
        "slug": "salgados",
        "titulo": "Salgados",
        "descricao": "",
    },
    {
        "slug": "bebidas",
        "titulo": "Bebidas",
        "descricao": "",
    },
]


# ============================================================
# PRODUTOS INICIAIS
# ============================================================

PRODUTOS_INICIAIS = [
    {
        "id": "palha-italiana",
        "nome": "Palha italiana",
        "desc": "Cremosa e muito saborosa, nossa palha italiana vai deixar seu dia mais feliz e mais leve.",
        "preco": 6.00,
        "imagem": "imagens/palha-italiana.jpg",
        "categoria": "doces",
        "tags": ["Novidade", "Promoção"],
    },
    {
        "id": "cookie-nutella",
        "nome": "Cookie recheado de Nutella",
        "desc": "Cookie macio com casca levemente crocante e generoso recheio cremoso de Nutella.",
        "preco": 10.00,
        "imagem": "imagens/cookie-nutella.jpg",
        "categoria": "doces",
        "tags": ["Novidade"],
    },
    {
        "id": "cookie-kinder-bueno",
        "nome": "Cookie Kinder Bueno",
        "desc": "Nossa já consagrada massa de cookie acompanhada com recheio Caribe Bueno da Master Martini, cremoso e com pedacinhos de avelã.",
        "preco": 10.00,
        "imagem": "imagens/cookie-kinder-bueno.jpg",
        "categoria": "doces",
        "tags": [],
    },
    {
        "id": "ninho-nutella",
        "nome": "Brownie Ninho com Nutella",
        "desc": "Se você deseja experimentar um pedaço do céu. Essa é a sua melhor oportunidade. A Nutella cremosa combina perfeitamente com o sabor suave do leite Ninho.",
        "preco": 10.00,
        "imagem": "imagens/brownie-ninho-nutella.jpg",
        "categoria": "brownies-recheados",
        "tags": ["+ Vendido"],
    },
    {
        "id": "ferrero",
        "nome": "Ferrero",
        "desc": "Massa deliciosa da Mimi Brownies com um brigadeiro cremoso de chocolate e uma camada generosa de creme de avelã, inspirado no clássico Ferrero Rocher.",
        "preco": 10.00,
        "imagem": "imagens/brownie-ferrero.jpg",
        "categoria": "brownies-recheados",
        "tags": [],
    },
    {
        "id": "ninho-morango",
        "nome": "Brownie de ninho com morango",
        "desc": "Este brownie possui uma massa equilibrada nem muito doce nem muito amarga. Vem recheado com creme de Ninho e pedaços de morango fresco.",
        "preco": 10.00,
        "imagem": "imagens/brownie-ninho-morango.jpg",
        "categoria": "brownies-recheados",
        "tags": [],
    },
    {
        "id": "brownie-brigadeiro",
        "nome": "Brownie de Brigadeiro",
        "desc": "Um brigadeiro de chocolate meio amargo, com uma textura cremosa e o sabor do verdadeiro chocolate belga envolvido na massa de brownie.",
        "preco": 10.00,
        "imagem": "imagens/brownie-brigadeiro.jpg",
        "categoria": "brownies-recheados",
        "tags": [],
    },
    {
        "id": "bem-casado",
        "nome": "Brownie De Bem Casado",
        "desc": "Brownie de massa tradicional com o recheio que já ganhou o coração do brasileiro. Bem casado cremoso de leite em pó com casquinha fina de açúcar.",
        "preco": 10.00,
        "imagem": "imagens/brownie-bem-casado.jpg",
        "categoria": "brownies-recheados",
        "tags": [],
    },
    {
        "id": "brownie-beijinho",
        "nome": "Brownie de Beijinho",
        "desc": "Este é o queridinho da Mimi, um dos mais vendidos. É recheado com um brigadeiro de coco macio com cobertura de coco ralado fresco.",
        "preco": 10.00,
        "imagem": "imagens/brownie-beijinho.jpg",
        "categoria": "brownies-recheados",
        "tags": [],
    },
    {
        "id": "ninho",
        "nome": "Brownie de Ninho",
        "desc": "Brownie de massa equilibrada, nem muito doce e nem muito amarga. Recheado com o brigadeiro de leite Ninho cremoso e suave.",
        "preco": 10.00,
        "imagem": "imagens/brownie-ninho.jpg",
        "categoria": "brownies-recheados",
        "tags": [],
    },
    {
        "id": "choconinho-300ml",
        "nome": "Choconinho 300ml",
        "desc": "Um delicioso copo com 300ml de puro sabor, recheado com o nosso creme especial de ninho com cobertura de chocolate trufado.",
        "preco": 25.00,
        "imagem": "imagens/copo-choconinho.jpg",
        "categoria": "copo-da-felicidade",
        "tags": ["+ Vendido"],
    },
    {
        "id": "copo-explosao",
        "nome": "Copo explosão",
        "desc": "Nosso copo da felicidade de ninho com morango é uma experiência saborosa e divertida. Camadas de brownie, brigadeiro de Ninho, morangos frescos e granulado.",
        "preco": 22.00,
        "imagem": "imagens/copo-explosao.jpg",
        "categoria": "copo-da-felicidade",
        "tags": [],
    },
    {
        "id": "brownie-tradicional-10pts",
        "nome": "Brownie Tradicional 10pts",
        "desc": "O Brownie mais gostoso que você irá comer na sua vida. Super equilibrado, nem muito doce, nem muito amargo. Pedaço generoso de massa tradicional.",
        "preco": 7.00,
        "imagem": "imagens/brownie-tradicional.jpg",
        "categoria": "tradicional",
        "tags": [],
    },
    {
        "id": "casquinha-simples",
        "nome": "Casquinha simples",
        "desc": "A casquinha é a parte mais crocante e menos doce do brownie. É perfeita para acompanhar um café ou um sorvete.",
        "preco": 3.00,
        "imagem": "imagens/casquinha-simples.jpg",
        "categoria": "casquinha",
        "tags": [],
    },
    {
        "id": "casquinha-suprema",
        "nome": "Casquinha suprema",
        "desc": "A casquinha é um dos produtos mais amados que temos por aqui. E nessa versão cheia de brigadeiro cremoso, confeitos coloridos e cobertura especial.",
        "preco": 23.00,
        "imagem": "imagens/casquinha-suprema.jpg",
        "categoria": "casquinha",
        "tags": [],
    },
    {
        "id": "coxinha-frango",
        "nome": "Coxinha de frango",
        "desc": "Uma coxinha recheada com frango com um super tempero especial da casa, crocante por fora e macia por dentro.",
        "preco": 6.00,
        "imagem": "imagens/coxinha-frango.jpg",
        "categoria": "salgados",
        "tags": [],
    },
    {
        "id": "coxinha-frango-cream-cheese",
        "nome": "Coxinha de frango com cream cheese",
        "desc": "A nossa coxinha maravilhosa e super temperada de frango e com o recheio de cream cheese que derrete na boca.",
        "preco": 8.00,
        "imagem": "imagens/coxinha-cream-cheese.jpg",
        "categoria": "salgados",
        "tags": [],
    },
    {
        "id": "coca-lata",
        "nome": "Coca em Lata",
        "desc": "Refrigerante Coca-Cola em lata gelado de 350ml.",
        "preco": 6.00,
        "imagem": "imagens/coca-lata.jpg",
        "categoria": "bebidas",
        "tags": [],
    },
    {
        "id": "agua-sem-gas",
        "nome": "Água sem gás",
        "desc": "Água sem gás 500ml, perfeitamente gelada.",
        "preco": 2.00,
        "imagem": "imagens/agua-sem-gas.jpg",
        "categoria": "bebidas",
        "tags": [],
    },
]


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def extensao_permitida(nome_arquivo):
    return (
        "." in nome_arquivo
        and nome_arquivo.rsplit(".", 1)[1].lower()
        in EXTENSOES_PERMITIDAS
    )


def salvar_upload_imagem(arquivo, prefixo="produto"):
    if not arquivo or arquivo.filename == "":
        return None

    if not extensao_permitida(arquivo.filename):
        raise ValueError(
            "Tipo de arquivo inválido. "
            "Use PNG, JPG, JPEG, GIF ou WEBP."
        )

    nome_seguro = secure_filename(arquivo.filename)

    nome_base, ext = os.path.splitext(nome_seguro)

    timestamp = (
        f"{int(time.time())}-"
        f"{time.time_ns() % 1000000:06d}"
    )

    nome_final = (
        f"{prefixo}-{nome_base}-{timestamp}{ext}"
    ).lower()

    caminho_completo = os.path.join(
        PASTA_UPLOADS,
        nome_final
    )

    arquivo.save(caminho_completo)

    return f"imagens/{nome_final}"


def gerar_slug(texto):
    texto = unicodedata.normalize(
        "NFKD",
        texto
    ).encode(
        "ascii",
        "ignore"
    ).decode("ascii")

    caracteres = []

    for caractere in texto.lower():
        if caractere.isalnum():
            caracteres.append(caractere)
        elif caractere in (" ", "-", "_"):
            caracteres.append("-")

    slug = "".join(caracteres)

    while "--" in slug:
        slug = slug.replace("--", "-")

    return slug.strip("-")


def admin_requerido(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        if not session.get("admin_autenticado"):
            return redirect(
                url_for(
                    "login_admin",
                    next=request.path
                )
            )

        return funcao(*args, **kwargs)

    return wrapper


# ============================================================
# PRODUTOS
# ============================================================

def carregar_produtos():
    if not os.path.exists(ARQUIVO_PRODUTOS):
        salvar_produtos(PRODUTOS_INICIAIS)

    try:
        with open(
            ARQUIVO_PRODUTOS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except (
        json.JSONDecodeError,
        OSError
    ):
        salvar_produtos(PRODUTOS_INICIAIS)
        return PRODUTOS_INICIAIS


def salvar_produtos(produtos):
    with open(
        ARQUIVO_PRODUTOS,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            produtos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


# ============================================================
# CATEGORIAS
# ============================================================

def carregar_categorias():
    if not os.path.exists(ARQUIVO_CATEGORIAS):
        salvar_categorias(CATEGORIAS_INICIAIS)

    try:
        with open(
            ARQUIVO_CATEGORIAS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            categorias = json.load(arquivo)

            if not isinstance(categorias, list):
                raise ValueError

            return categorias

    except (
        json.JSONDecodeError,
        OSError,
        ValueError
    ):
        salvar_categorias(CATEGORIAS_INICIAIS)
        return CATEGORIAS_INICIAIS


def salvar_categorias(categorias):
    with open(
        ARQUIVO_CATEGORIAS,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            categorias,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route("/")
def pagina_inicial():
    produtos = carregar_produtos()
    categorias = carregar_categorias()

    return render_template(
        "index.html",
        marca=NOME_DA_MARCA,
        whatsapp=WHATSAPP,
        instagram_usuario=INSTAGRAM_USUARIO,
        instagram_link=INSTAGRAM_LINK,
        cidade_regiao=CIDADE_REGIAO,
        info_entrega=INFO_ENTREGA,
        hero_titulo=HERO_TITULO,
        hero_texto=HERO_TEXTO,
        sobre_titulo=SOBRE_TITULO,
        sobre_texto=SOBRE_TEXTO,
        endereco_loja=ENDERECO_LOJA,
        tempo_medio_delivery=TEMPO_MEDIO_DELIVERY,
        tempo_medio_balcao=TEMPO_MEDIO_BALCAO,
        recompensas_fidelidade=RECOMPENSAS_FIDELIDADE,
        horarios_funcionamento=HORARIOS_FUNCIONAMENTO,
        metodos_pagamento=METODOS_PAGAMENTO,
        taxas_entrega=TAXAS_ENTREGA,
        categorias_produtos=categorias,
        produtos=produtos,
    )


# ============================================================
# GERAR PEDIDO
# ============================================================

@app.route("/gerar-pedido", methods=["POST"])
def gerar_pedido():
    dados = request.get_json()

    if not dados or "itens" not in dados:
        return jsonify({
            "erro": "Pedido vazio."
        }), 400

    nome = dados.get(
        "nome",
        ""
    ).strip()

    if not nome:
        return jsonify({
            "erro": "Informe seu nome."
        }), 400

    itens_recebidos = dados["itens"]

    if (
        not isinstance(itens_recebidos, list)
        or len(itens_recebidos) == 0
    ):
        return jsonify({
            "erro": "Nenhum item no pedido."
        }), 400

    produtos = carregar_produtos()

    produtos_por_id = {
        produto["id"]: produto
        for produto in produtos
    }

    mensagem_linhas = []
    total = 0.0

    for item in itens_recebidos:
        produto_id = item.get("id")
        quantidade = item.get("quantidade", 0)

        if produto_id not in produtos_por_id:
            return jsonify({
                "erro": f"Produto inválido: {produto_id}"
            }), 400

        try:
            quantidade = int(quantidade)
        except (
            ValueError,
            TypeError
        ):
            return jsonify({
                "erro": "Quantidade inválida."
            }), 400

        if quantidade < 1 or quantidade > 999:
            return jsonify({
                "erro": "Quantidade deve ser entre 1 e 999."
            }), 400

        produto = produtos_por_id[produto_id]

        preco = float(produto["preco"])

        subtotal = preco * quantidade

        total += subtotal

        mensagem_linhas.append(
            f"{quantidade}x {produto['nome']} — "
            f"R$ {subtotal:.2f}"
        )

    texto_itens = "\n".join(
        mensagem_linhas
    )

    mensagem = (
        f"Olá! Meu nome é {nome} "
        f"e gostaria de fazer um pedido:\n\n"
        f"{texto_itens}\n\n"
        f"Total: R$ {total:.2f}\n\n"
        "Gostaria de saber sobre a entrega."
    )

    mensagem_codificada = urllib.parse.quote(
        mensagem
    )

    link_whatsapp = (
        f"https://wa.me/{WHATSAPP}"
        f"?text={mensagem_codificada}"
    )

    return jsonify({
        "link": link_whatsapp,
        "total": f"R$ {total:.2f}"
    })


# ============================================================
# LOGIN / LOGOUT
# ============================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def login_admin():
    proxima_pagina = (
        request.form.get("next")
        or request.args.get("next")
        or url_for("painel_admin")
    )

    erro = None

    if not proxima_pagina.startswith("/"):
        proxima_pagina = url_for(
            "painel_admin"
        )

    if request.method == "POST":
        senha_digitada = request.form.get(
            "senha",
            ""
        )

        if senha_digitada == SENHA_ADMIN:
            session["admin_autenticado"] = True

            return redirect(
                proxima_pagina
            )

        erro = "Senha incorreta. Tente novamente."

    return render_template(
        "admin_login.html",
        marca=NOME_DA_MARCA,
        next=proxima_pagina,
        erro=erro
    )


@app.route(
    "/admin/logout",
    methods=["POST"]
)
@admin_requerido
def logout_admin():
    session.pop(
        "admin_autenticado",
        None
    )

    return redirect(
        url_for("pagina_inicial")
    )


# ============================================================
# PAINEL ADMIN
# ============================================================

@app.route("/admin")
@admin_requerido
def painel_admin():
    produtos = carregar_produtos()
    categorias = carregar_categorias()

    return render_template(
        "admin.html",
        marca=NOME_DA_MARCA,
        produtos=produtos,
        categorias=categorias
    )


# ============================================================
# CRIAR CATEGORIA
# ============================================================

@app.route(
    "/admin/categoria/adicionar",
    methods=["POST"]
)
@admin_requerido
def adicionar_categoria():
    titulo = request.form.get(
        "titulo",
        ""
    ).strip()

    descricao = request.form.get(
        "descricao",
        ""
    ).strip()

    if not titulo:
        return (
            "O nome da categoria é obrigatório.",
            400
        )

    slug_base = gerar_slug(titulo)

    if not slug_base:
        return (
            "Nome de categoria inválido.",
            400
        )

    categorias = carregar_categorias()

    if any(
        categoria["slug"] == slug_base
        for categoria in categorias
    ):
        return (
            "Já existe uma categoria com esse nome.",
            400
        )

    nova_categoria = {
        "slug": slug_base,
        "titulo": titulo,
        "descricao": descricao,
    }

    categorias.append(
        nova_categoria
    )

    salvar_categorias(categorias)

    return redirect(
        url_for("painel_admin")
    )


# ============================================================
# EXCLUIR CATEGORIA
# ============================================================

@app.route(
    "/admin/categoria/excluir/<slug>",
    methods=["POST"]
)
@admin_requerido
def excluir_categoria(slug):
    categorias = carregar_categorias()
    produtos = carregar_produtos()

    possui_produtos = any(
        produto.get("categoria") == slug
        for produto in produtos
    )

    if possui_produtos:
        return (
            "Não é possível excluir esta categoria "
            "porque existem produtos dentro dela. "
            "Mova ou exclua os produtos primeiro.",
            400
        )

    categorias_filtradas = [
        categoria
        for categoria in categorias
        if categoria["slug"] != slug
    ]

    if len(categorias_filtradas) == len(categorias):
        return (
            "Categoria não encontrada.",
            404
        )

    salvar_categorias(
        categorias_filtradas
    )

    return redirect(
        url_for("painel_admin")
    )


# ============================================================
# ADICIONAR PRODUTO
# ============================================================

@app.route(
    "/admin/adicionar",
    methods=["POST"]
)
@admin_requerido
def adicionar_produto():
    nome = request.form.get(
        "nome",
        ""
    ).strip()

    descricao = request.form.get(
        "descricao",
        ""
    ).strip()

    preco = request.form.get(
        "preco",
        ""
    ).strip()

    categoria = request.form.get(
        "categoria",
        ""
    ).strip()

    tags_brutas = request.form.get(
        "tags",
        ""
    ).strip()

    tags = [
        t.strip()
        for t in tags_brutas.split(",")
        if t.strip()
    ]

    if not nome:
        return (
            "O nome do produto é obrigatório.",
            400
        )

    if not descricao:
        return (
            "A descrição do produto é obrigatória.",
            400
        )

    try:
        preco = float(
            preco.replace(",", ".")
        )
    except ValueError:
        return "Preço inválido.", 400

    if preco <= 0:
        return (
            "O preço deve ser maior que zero.",
            400
        )

    categorias = carregar_categorias()

    slugs_categorias = {
        categoria["slug"]
        for categoria in categorias
    }

    if categoria not in slugs_categorias:
        return (
            "Categoria inválida.",
            400
        )

    produtos = carregar_produtos()

    produto_id = gerar_slug(nome)

    if not produto_id:
        return (
            "Não foi possível gerar o ID do produto.",
            400
        )

    id_original = produto_id
    contador = 2

    while any(
        produto["id"] == produto_id
        for produto in produtos
    ):
        produto_id = (
            f"{id_original}-{contador}"
        )
        contador += 1

    try:
        imagem = salvar_upload_imagem(
            request.files.get("imagem"),
            prefixo=produto_id
        )
    except ValueError as erro:
        return str(erro), 400

    if not imagem:
        imagem = (
            "imagens/brownie-tradicional.jpg"
        )

    novo_produto = {
        "id": produto_id,
        "nome": nome,
        "desc": descricao,
        "preco": preco,
        "imagem": imagem,
        "categoria": categoria,
        "tags": tags,
    }

    produtos.append(
        novo_produto
    )

    salvar_produtos(produtos)

    return redirect(
        url_for("painel_admin")
    )


# ============================================================
# EDITAR PRODUTO
# ============================================================

@app.route(
    "/admin/editar/<produto_id>",
    methods=["GET"]
)
@admin_requerido
def form_editar_produto(produto_id):
    produtos = carregar_produtos()
    categorias = carregar_categorias()

    produto = None

    for p in produtos:
        if p["id"] == produto_id:
            produto = p
            break

    if produto is None:
        return (
            "Produto não encontrado.",
            404
        )

    return render_template(
        "admin_editar.html",
        marca=NOME_DA_MARCA,
        produto=produto,
        categorias=categorias
    )


@app.route(
    "/admin/editar/<produto_id>",
    methods=["POST"]
)
@admin_requerido
def salvar_edicao_produto(produto_id):
    nome = request.form.get(
        "nome",
        ""
    ).strip()

    descricao = request.form.get(
        "descricao",
        ""
    ).strip()

    preco = request.form.get(
        "preco",
        ""
    ).strip()

    categoria = request.form.get(
        "categoria",
        ""
    ).strip()

    tags_brutas = request.form.get(
        "tags",
        ""
    ).strip()

    tags = [
        t.strip()
        for t in tags_brutas.split(",")
        if t.strip()
    ]

    if not nome:
        return (
            "O nome do produto é obrigatório.",
            400
        )

    if not descricao:
        return (
            "A descrição do produto é obrigatória.",
            400
        )

    try:
        preco = float(
            preco.replace(",", ".")
        )
    except ValueError:
        return "Preço inválido.", 400

    if preco <= 0:
        return (
            "O preço deve ser maior que zero.",
            400
        )

    categorias = carregar_categorias()

    slugs_categorias = {
        item["slug"]
        for item in categorias
    }

    if categoria not in slugs_categorias:
        return (
            "Categoria inválida.",
            400
        )

    produtos = carregar_produtos()

    encontrado = False

    for produto in produtos:
        if produto["id"] != produto_id:
            continue

        produto["nome"] = nome
        produto["desc"] = descricao
        produto["preco"] = preco
        produto["categoria"] = categoria
        produto["tags"] = tags

        try:
            nova_imagem = salvar_upload_imagem(
                request.files.get("imagem"),
                prefixo=produto_id
            )
        except ValueError as erro:
            return str(erro), 400

        if nova_imagem:
            imagem_antiga_rel = produto.get(
                "imagem",
                ""
            )

            caminho_antiga = os.path.join(
                app.root_path,
                "static",
                imagem_antiga_rel
            )

            produto["imagem"] = nova_imagem

            if (
                "brownie-tradicional"
                not in imagem_antiga_rel
                and os.path.exists(caminho_antiga)
            ):
                try:
                    os.remove(
                        caminho_antiga
                    )
                except OSError:
                    pass

        encontrado = True
        break

    if not encontrado:
        return (
            "Produto não encontrado.",
            404
        )

    salvar_produtos(produtos)

    return redirect(
        url_for("painel_admin")
    )


# ============================================================
# EXCLUIR PRODUTO
# ============================================================

@app.route(
    "/admin/excluir/<produto_id>",
    methods=["POST"]
)
@admin_requerido
def excluir_produto(produto_id):
    produtos = carregar_produtos()

    produto_removido = None

    produtos_filtrados = []

    for produto in produtos:
        if produto["id"] == produto_id:
            produto_removido = produto
        else:
            produtos_filtrados.append(
                produto
            )

    if produto_removido:
        imagem = produto_removido.get(
            "imagem",
            ""
        )

        if (
            imagem
            and "brownie-tradicional"
            not in imagem
        ):
            caminho = os.path.join(
                app.root_path,
                "static",
                imagem
            )

            if os.path.exists(caminho):
                try:
                    os.remove(caminho)
                except OSError:
                    pass

    salvar_produtos(
        produtos_filtrados
    )

    return redirect(
        url_for("painel_admin")
    )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)