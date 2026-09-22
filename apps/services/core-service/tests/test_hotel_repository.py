from app.models.hotel import Cidade
from app.repositories.hotel_repository import CidadeRepository


def test_listar_cidades_em_ordem_alfabetica(db_session):
    db_session.add_all(
        [
            Cidade(nome="Sobral"),
            Cidade(nome="Fortaleza"),
            Cidade(nome="Quixada"),
        ]
    )
    db_session.commit()

    repo = CidadeRepository(db_session)
    cidades = repo.list()

    assert [cidade.nome for cidade in cidades] == [
        "Fortaleza",
        "Quixada",
        "Sobral",
    ]


def test_criar_cidade_no_repository(db_session):
    repo = CidadeRepository(db_session)

    cidade = repo.create(nome="Crato")

    assert cidade.id is not None
    assert cidade.nome == "Crato"

    cidade_salva = (
        db_session.query(Cidade)
        .filter(Cidade.id == cidade.id)
        .first()
    )

    assert cidade_salva is not None
    assert cidade_salva.nome == "Crato"


def test_buscar_cidade_por_id_no_repository(db_session):
    repo = CidadeRepository(db_session)
    cidade_criada = repo.create(nome="Iguatu")

    cidade_encontrada = repo.get_by_id(cidade_criada.id)

    assert cidade_encontrada is not None
    assert cidade_encontrada.id == cidade_criada.id
    assert cidade_encontrada.nome == "Iguatu"


def test_buscar_cidade_por_nome_no_repository(db_session):
    repo = CidadeRepository(db_session)
    repo.create(nome="Juazeiro do Norte")

    cidade_encontrada = repo.get_by_nome("Juazeiro do Norte")

    assert cidade_encontrada is not None
    assert cidade_encontrada.nome == "Juazeiro do Norte"