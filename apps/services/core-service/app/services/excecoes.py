"""Excecoes de dominio dos services.

Nao herdam de HTTPException de proposito: o service nao conhece HTTP. Quem
traduz cada uma em status code e a camada de rota. Ficam num modulo so para
que exista UMA classe por regra: um ``except CidadeNaoEncontradaError`` precisa
capturar o erro venha ele do CidadeService ou do HotelService.
"""


class RegraDeNegocioError(Exception):
    """Base das excecoes de negocio."""


class CidadeJaExisteError(RegraDeNegocioError):
    pass


class CidadeNaoEncontradaError(RegraDeNegocioError):
    pass


class HotelNaoEncontradoError(RegraDeNegocioError):
    pass
