import uuid

from app.models.tutorial import Linguagem, Stack, Tecnologia
from app.repositories.tutorial_repository import TutorialRepository
from app.repositories.usuario_repository import UsuarioRepository


def test_create_professor_in_repository(db_session):
    repo = TutorialRepository(db_session)
    prof = repo.create_professor(
        nome="Professor de Teste",
        email="teste@unicatolica.edu.br",
        sala="Sala Teste, Bloco T",
        biografia="Uma biografia de teste.",
        biografia_mapa={"orcid": "0000-0001-2345-6789"},
    )

    assert prof.id is not None
    assert prof.nome == "Professor de Teste"
    assert prof.email == "teste@unicatolica.edu.br"
    assert prof.detalhe is not None
    assert prof.detalhe.sala == "Sala Teste, Bloco T"
    assert prof.detalhe.biografia == "Uma biografia de teste."
    assert prof.detalhe.biografia_mapa == {"orcid": "0000-0001-2345-6789"}


def test_get_professor_by_id_in_repository(db_session):
    repo = TutorialRepository(db_session)
    created_prof = repo.create_professor(
        nome="Outro Prof",
        email="outro@unicatolica.edu.br",
        sala="Sala B",
    )

    fetched_prof = repo.get_professor_by_id(created_prof.id)
    assert fetched_prof is not None
    assert fetched_prof.id == created_prof.id
    assert fetched_prof.nome == "Outro Prof"
    assert repo.get_professor_by_id(uuid.uuid4()) is None


def test_get_professor_with_details_e_disciplinas(db_session):
    repo = TutorialRepository(db_session)
    prof = repo.create_professor(
        nome="Docente Web",
        email="docente.web@unicatolica.edu.br",
        sala="Lab 02",
        biografia="Especialista em Arquitetura Web",
    )

    disc = repo.create_disciplina(
        nome="Programacao Web",
        ano=2026,
        semestre=2,
        professor_id=str(prof.id),
    )

    assert disc.id is not None
    assert disc.professor_id == prof.id

    professores = repo.get_professor_with_details()
    assert len(professores) == 1
    assert professores[0].nome == "Docente Web"
    assert professores[0].detalhe.sala == "Lab 02"
    assert len(professores[0].disciplinas) == 1
    assert professores[0].disciplinas[0].nome == "Programacao Web"


def test_get_stacks_with_tecnologias_e_linguagens(db_session):
    repo = TutorialRepository(db_session)
    python = Linguagem(nome="Python")
    javascript = Linguagem(nome="JavaScript")
    fastapi = Tecnologia(nome="FastAPI", linguagens=[python])
    react = Tecnologia(nome="React", linguagens=[javascript])

    db_session.add_all(
        [
            Stack(nome="Backend", tecnologias=[fastapi]),
            Stack(nome="Frontend", tecnologias=[react]),
        ]
    )
    db_session.commit()

    stacks = repo.get_stacks_with_tecnologias()
    nomes_stacks = sorted([st.nome for st in stacks])
    assert nomes_stacks == ["Backend", "Frontend"]

    mapa = {st.nome: st for st in stacks}
    assert mapa["Backend"].tecnologias[0].nome == "FastAPI"
    assert mapa["Backend"].tecnologias[0].linguagens[0].nome == "Python"
    assert mapa["Frontend"].tecnologias[0].nome == "React"
    assert mapa["Frontend"].tecnologias[0].linguagens[0].nome == "JavaScript"


def test_usuario_repository_create_e_busca_por_email(db_session):
    repo = UsuarioRepository(db_session)

    assert repo.email_exists("novo.aluno@unicatolica.edu.br") is False
    assert repo.get_by_email("novo.aluno@unicatolica.edu.br") is None

    usuario = repo.create(
        nome="Julio Henrique",
        email="novo.aluno@unicatolica.edu.br",
        senha_hash="hash_seguro_bcrypt",
        is_admin=False,
    )

    assert usuario.id is not None
    assert usuario.nome == "Julio Henrique"
    assert usuario.is_admin is False
    assert repo.email_exists("novo.aluno@unicatolica.edu.br") is True

    encontrado = repo.get_by_email("novo.aluno@unicatolica.edu.br")
    assert encontrado is not None
    assert encontrado.id == usuario.id
    assert encontrado.senha_hash == "hash_seguro_bcrypt"


def test_usuario_repository_create_admin(db_session):
    repo = UsuarioRepository(db_session)
    admin = repo.create(
        nome="Admin Echo",
        email="admin.echo@unicatolica.edu.br",
        senha_hash="hash_admin_bcrypt",
        is_admin=True,
    )

    assert admin.is_admin is True
    encontrado = repo.get_by_email("admin.echo@unicatolica.edu.br")
    assert encontrado is not None
    assert encontrado.is_admin is True
