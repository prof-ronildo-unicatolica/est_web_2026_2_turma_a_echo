from sqlalchemy import inspect

from app.models.hotel import Cidade, Hotel
from app.repositories.cidade_repository import CidadeRepository
from app.repositories.hotel_repository import HotelRepository


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

    cidade_salva = db_session.query(Cidade).filter(Cidade.id == cidade.id).first()

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


def test_listar_hoteis_com_cidade_carregada(db_session):
    cidade = Cidade(nome="Fortaleza")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    repo = HotelRepository(db_session)

    repo.create(
        Hotel(
            nome="Hotel Z",
            cidade_id=cidade.id,
            estrelas=4,
        )
    )

    repo.create(
        Hotel(
            nome="Hotel A",
            cidade_id=cidade.id,
            estrelas=5,
        )
    )

    db_session.expire_all()

    hoteis = repo.list()

    assert [hotel.nome for hotel in hoteis] == ["Hotel A", "Hotel Z"]

    for hotel in hoteis:
        assert "cidade" not in inspect(hotel).unloaded
        assert hotel.cidade.nome == "Fortaleza"


def test_listar_hoteis_por_cidade(db_session):
    fortaleza = Cidade(nome="Fortaleza")
    sobral = Cidade(nome="Sobral")

    db_session.add_all([fortaleza, sobral])
    db_session.commit()

    repo = HotelRepository(db_session)

    repo.create(
        Hotel(
            nome="Hotel Fortaleza",
            cidade_id=fortaleza.id,
            estrelas=4,
        )
    )

    repo.create(
        Hotel(
            nome="Hotel Sobral",
            cidade_id=sobral.id,
            estrelas=3,
        )
    )

    db_session.expire_all()

    hoteis = repo.list_by_cidade(fortaleza.id)

    assert len(hoteis) == 1
    assert hoteis[0].nome == "Hotel Fortaleza"
    assert "cidade" not in inspect(hoteis[0]).unloaded
    assert hoteis[0].cidade.nome == "Fortaleza"


def test_buscar_hotel_por_id_com_cidade_carregada(db_session):
    cidade = Cidade(nome="Quixada")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    repo = HotelRepository(db_session)

    hotel_criado = repo.create(
        Hotel(
            nome="Hotel Quixada",
            cidade_id=cidade.id,
            estrelas=5,
        )
    )

    hotel_id = hotel_criado.id

    db_session.expire_all()

    hotel = repo.get_by_id(hotel_id)

    assert hotel is not None
    assert hotel.nome == "Hotel Quixada"
    assert "cidade" not in inspect(hotel).unloaded
    assert hotel.cidade.nome == "Quixada"
