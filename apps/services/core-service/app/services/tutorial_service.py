import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.core.rabbitmq import publish_event
from app.models.tutorial import Disciplina, Professor
from app.repositories.tutorial_repository import TutorialRepository


def _normalizar_texto(valor: str | None) -> str:
    if valor is None:
        return ""
    return valor.strip()


class TutorialService:
    def __init__(self, db: Session):
        self.repository = TutorialRepository(db)

    def _serializar_professor(self, prof: Professor) -> dict[str, Any]:
        detalhe = prof.detalhe
        biografia_mapa = (
            detalhe.biografia_mapa
            if (detalhe is not None and detalhe.biografia_mapa)
            else None
        )
        return {
            "nome": prof.nome,
            "email": prof.email,
            "sala": detalhe.sala if detalhe is not None else "",
            "biografia": (
                detalhe.biografia
                if (detalhe is not None and detalhe.biografia is not None)
                else ""
            ),
            "biografia_mapa": biografia_mapa,
        }

    def _serializar_disciplinas(self, prof: Professor) -> list[dict[str, Any]]:
        resultado: list[dict[str, Any]] = []
        for disc in prof.disciplinas:
            resultado.append(
                {
                    "nome": disc.nome,
                    "ano": disc.ano,
                    "semestre": disc.semestre,
                    "tecnologias": [t.nome for t in disc.tecnologias],
                }
            )
        return resultado

    def list_stacks_resumo(self) -> list[dict[str, Any]]:
        stacks = self.repository.get_stacks_with_tecnologias()
        resultado: list[dict[str, Any]] = []
        for st in stacks:
            stack_data: dict[str, Any] = {"nome": st.nome, "tecnologias": []}
            for tech in st.tecnologias:
                stack_data["tecnologias"].append(
                    {
                        "nome": tech.nome,
                        "linguagens": [lang.nome for lang in tech.linguagens],
                    }
                )
            resultado.append(stack_data)
        return resultado

    def get_sobre_data(self) -> dict[str, Any]:
        professores = self.repository.get_professor_with_details()

        equipe_info: dict[str, Any] = {
            "equipe": "Echo",
            "ano": 2026,
            "semestre": 2,
            "professor": None,
            "disciplinas": [],
            "stacks": self.list_stacks_resumo(),
        }

        if professores:
            prof = professores[0]
            equipe_info["professor"] = self._serializar_professor(prof)
            equipe_info["disciplinas"] = self._serializar_disciplinas(prof)

        return equipe_info

    def get_professor_by_id(
        self, professor_id: uuid.UUID | str
    ) -> dict[str, Any] | None:
        if isinstance(professor_id, str):
            try:
                professor_id = uuid.UUID(professor_id)
            except ValueError:
                return None

        prof = self.repository.get_professor_by_id(professor_id)
        if prof is None:
            return None

        return self._serializar_professor(prof)

    def create_professor(self, payload: Any) -> dict[str, Any]:
        nome = _normalizar_texto(payload.nome)
        email = _normalizar_texto(payload.email)
        sala = _normalizar_texto(payload.sala)
        if not nome or not email or not sala:
            raise ValueError("Nome, email e sala do professor sao obrigatorios.")

        biografia = getattr(payload, "biografia", None)
        biografia_mapa = getattr(payload, "biografia_mapa", None)
        prof = self.repository.create_professor(
            nome=nome,
            email=email,
            sala=sala,
            biografia=biografia,
            biografia_mapa=biografia_mapa,
        )
        return self._serializar_professor(prof)

    async def create_disciplina(self, payload: Any) -> Disciplina:
        nome = _normalizar_texto(payload.nome)
        if not nome:
            raise ValueError("O nome da disciplina nao pode ser vazio.")

        disciplina = self.repository.create_disciplina(
            nome=nome,
            ano=payload.ano,
            semestre=payload.semestre,
            professor_id=payload.professor_id,
        )

        event_data = {
            "evento": "disciplina.criada",
            "disciplina_id": str(disciplina.id),
            "nome": disciplina.nome,
            "ano": disciplina.ano,
            "semestre": disciplina.semestre,
            "professor_id": str(disciplina.professor_id),
        }
        await publish_event("audit.logs", event_data)

        return disciplina
