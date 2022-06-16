from abc import abstractmethod
from os import getenv, curdir
from os.path import isfile, join

from screening.models.log import Log
from screening.utils.singleton import Singleton


class Configuracoes(metaclass=Singleton):
    """
    Configurações para realização da análise de contingências.
    """
    def __init__(self) -> None:
        self._arquivo_usinas = None
        self._arquivo_dados = None
        self._arquivo_shapefile = None

    @property
    def arquivo_usinas(self) -> str:
        """
        Caminho relativo até o arquivo com cadastro das usinas.

        :return: Caminho relativo em unix-style
        :rtype: str
        """
        return self._arquivo_usinas

    @property
    def arquivo_dados(self) -> str:
        """
        Caminho relativo até o arquivo com dados de vento das usinas.

        :return: Caminho relativo em unix-style
        :rtype: str
        """
        return self._arquivo_dados

    @property
    def arquivo_shapefile(self) -> str:
        """
        Caminho relativo até o arquivo com formas dos estados.

        :return: Caminho relativo em unix-style
        :rtype: str
        """
        return self._arquivo_shapefile

    @classmethod
    def le_variaveis_ambiente(cls) -> "Configuracoes":
        cb = BuilderConfiguracoesENV()
        c = cb.arquivo_usinas("ARQUIVO_USINAS")\
            .arquivo_dados("ARQUIVO_DADOS")\
            .arquivo_shapefile("ARQUIVO_SHAPEFILE")\
            .build()
        return c


class BuilderConfiguracoes:
    """
    Interface genérica para implementação do padrão Builder
    para a classe de Configurações.
    """
    def __init__(self,
                 configuracoes: Configuracoes):
        self._configuracoes = configuracoes
        self._log = Log.log()

    def build(self) -> Configuracoes:
        return self._configuracoes

    @abstractmethod
    def arquivo_usinas(self, variavel: str):
        pass

    @abstractmethod
    def arquivo_dados(self, variavel: str):
        pass

    @abstractmethod
    def arquivo_shapefile(self, variavel: str):
        pass


class BuilderConfiguracoesENV(BuilderConfiguracoes):
    """
    Implementação do padrão builder para as configurações,
    no caso da construção a partir de variáveis de ambiente.
    """
    def __init__(self,
                 configuracoes: Configuracoes=Configuracoes()):
        super().__init__(configuracoes=configuracoes)

    @staticmethod
    def __le_e_confere_variavel(variavel: str):
        # Lê a variável de ambiente
        valor = getenv(variavel)
        # Valida o conteúdo
        if valor is None:
            raise ValueError(f"Variável {variavel} não encontrada")
        return valor

    @staticmethod
    def __valida_int(variavel: str):
        try:
            valor = int(variavel)
            valorfloat = float(variavel)
            if valor != valorfloat:
                raise ValueError()
        except ValueError:
            raise ValueError(f"Variável {variavel} não é inteira")
        return valor

    @staticmethod
    def __valida_float(variavel: str):
        try:
            valor = float(variavel)
        except ValueError:
            raise ValueError(f"Variável {variavel} não é real")
        return valor

    def arquivo_usinas(self, variavel: str):
        valor = BuilderConfiguracoesENV.__le_e_confere_variavel(variavel)
        # Confere se existe o arquivo no diretorio raiz de encadeamento
        if not isfile(join(curdir, valor)):
            raise FileNotFoundError("Arquivo com as usinas não " +
                                    f"encontrado: {valor}")
        self._configuracoes._arquivo_usinas = valor
        # Fluent method
        self._log.info(f"Arquivo com usinas: {valor}")
        return self

    def arquivo_dados(self, variavel: str):
        valor = BuilderConfiguracoesENV.__le_e_confere_variavel(variavel)
        # Confere se existe o arquivo no diretorio raiz de encadeamento
        if not isfile(join(curdir, valor)):
            raise FileNotFoundError("Arquivo com os dados não " +
                                    f"encontrado: {valor}")
        self._configuracoes._arquivo_dados = valor
        # Fluent method
        self._log.info(f"Arquivo com dados: {valor}")
        return self

    def arquivo_shapefile(self, variavel: str):
        valor = BuilderConfiguracoesENV.__le_e_confere_variavel(variavel)
        # Confere se existe o arquivo no diretorio raiz de encadeamento
        if not isfile(join(curdir, valor)):
            raise FileNotFoundError("Arquivo com as formas não " +
                                    f"encontrado: {valor}")
        self._configuracoes._arquivo_shapefile = valor
        # Fluent method
        self._log.info(f"Arquivo com formas dos estados: {valor}")
        return self
