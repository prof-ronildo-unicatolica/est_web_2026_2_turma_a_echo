import uuid
from typing import Any

from sqlalchemy.orm import Session, joinedload

from app.models.tutorial import (
    Disciplina,
    Linguagem,
    Professor,
    ProfessorDetail,
    Stack,
    Tecnologia,
)


class TutorialRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_professor_with_details(self) -> list[Professor]:
        return (
            self.db.query(Professor)
            .options(
                joinedload(Professor.detalhe),
                joinedload(Professor.disciplinas).joinedload(Disciplina.tecnologias),
            )
            .all()
        )

    def get_stacks_with_tecnologias(self) -> list[Stack]:
        return (
            self.db.query(Stack)
            .options(joinedload(Stack.tecnologias).joinedload(Tecnologia.linguagens))
            .order_by(Stack.nome)
            .all()
        )

    def get_stack_by_nome(self, nome: str) -> Stack | None:
        return (
            self.db.query(Stack)
            .options(joinedload(Stack.tecnologias).joinedload(Tecnologia.linguagens))
            .filter(Stack.nome == nome.strip())
            .first()
        )

    def create_stack(self, nome: str) -> Stack:
        stack = Stack(nome=nome.strip())
        self.db.add(stack)
        self.db.commit()
        self.db.refresh(stack)
        return stack

    def list_tecnologias(self) -> list[Tecnologia]:
        return (
            self.db.query(Tecnologia)
            .options(
                joinedload(Tecnologia.stack),
                joinedload(Tecnologia.linguagens),
            )
            .order_by(Tecnologia.nome)
            .all()
        )

    def list_linguagens(self) -> list[Linguagem]:
        return self.db.query(Linguagem).order_by(Linguagem.nome).all()

    def get_professor_by_id(self, professor_id: Any) -> Professor | None:
        if isinstance(professor_id, str):
            try:
                professor_id = uuid.UUID(professor_id)
            except ValueError:
                return None

        return (
            self.db.query(Professor)
            .options(
                joinedload(Professor.detalhe),
                joinedload(Professor.disciplinas).joinedload(Disciplina.tecnologias),
            )
            .filter(Professor.id == professor_id)
            .first()
        )

    def get_professor_by_email(self, email: str) -> Professor | None:
        return (
            self.db.query(Professor)
            .options(joinedload(Professor.detalhe))
            .filter(Professor.email == email.strip())
            .first()
        )

    def create_professor(
        self,
        nome: str,
        email: str,
        sala: str,
        biografia: str | None = None,
        biografia_mapa: dict[str, Any] | None = None,
    ) -> Professor:
        prof = Professor(nome=nome, email=email)
        self.db.add(prof)
        self.db.flush()

        detail = ProfessorDetail(
            professor_id=prof.id,
            sala=sala,
            biografia=biografia,
            biografia_mapa=biografia_mapa,
        )
        self.db.add(detail)
        self.db.commit()
        self.db.refresh(prof)
        return prof

    def list_disciplinas(
        self, professor_id: uuid.UUID | None = None
    ) -> list[Disciplina]:
        query = self.db.query(Disciplina).options(
            joinedload(Disciplina.tecnologias),
            joinedload(Disciplina.professor),
        )
        if professor_id is not None:
            query = query.filter(Disciplina.professor_id == professor_id)
        return query.order_by(Disciplina.nome).all()

    def create_disciplina(
        self,
        nome: str,
        ano: int,
        semestre: int,
        professor_id: Any,
    ) -> Disciplina:
        if isinstance(professor_id, str):
            professor_id = uuid.UUID(professor_id)
        disciplina = Disciplina(
            nome=nome,
            ano=ano,
            semestre=semestre,
            professor_id=professor_id,
        )
        self.db.add(disciplina)
        self.db.commit()
        self.db.refresh(disciplina)
        return disciplina
