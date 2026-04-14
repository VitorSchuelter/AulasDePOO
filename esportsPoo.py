class Jogador:
    def __init__(self, nome, nickname, turma):
        self.nome = nome
        self.nickname = nickname
        self.turma = turma
        self.equipe = None

    def exibir(self):
        equipe_info = f" | Equipe: {self.equipe.nome}" if self.equipe else " | Sem equipe"
        print(f"  {self.nome} ({self.nickname}) - {self.turma}{equipe_info}")


class Equipe:
    LIMITE_JOGADORES = 5

    def __init__(self, nome, jogo):
        self.nome = nome
        self.jogo = jogo
        self.jogadores = []

    def adicionarJogador(self, jogador):
        if len(self.jogadores) >= self.LIMITE_JOGADORES:
            print(f"A equipe '{self.nome}' já atingiu o limite de {self.LIMITE_JOGADORES} jogadores!")
            return False

        if jogador.equipe is not None:
            print(f"O jogador '{jogador.nickname}' já pertence à equipe '{jogador.equipe.nome}'!")
            return False

        self.jogadores.append(jogador)
        jogador.equipe = self
        return True

    def removerJogador(self, jogador):
        if jogador in self.jogadores:
            self.jogadores.remove(jogador)
            jogador.equipe = None
            return True
        return False

    def exibirResumo(self):
        print(f"  {self.nome} | Jogo: {self.jogo} | Jogadores: {len(self.jogadores)}/{self.LIMITE_JOGADORES}")

    def exibirJogadores(self):
        print(f"\n  Equipe: {self.nome} | Jogo: {self.jogo}")
        if not self.jogadores:
            print("  Nenhum jogador nesta equipe.")
        else:
            print("  Jogadores:")
            for j in self.jogadores:
                print(f"    - {j.nome} ({j.nickname}) - {j.turma}")

jogadores = []
equipes = []


def exibirMenu():
    print("\n========================================")
    print("  CAMPEONATO INTERCLASSE DE E-SPORTS")
    print("========================================")
    print("1. Cadastrar jogador")
    print("2. Cadastrar equipe")
    print("3. Adicionar jogador a uma equipe")
    print("4. Listar todas as equipes")
    print("5. Listar jogadores de uma equipe")
    print("6. Buscar jogador por nickname")
    print("7. Remover jogador de uma equipe")  # Desafio extra
    print("0. Sair")
    print("========================================")


def cadastrarJogador():
    print("\n--- Cadastrar Jogador ---")
    nome = input("Nome: ").strip()
    nickname = input("Nickname: ").strip()

    # Desafio extra: impedir nickname duplicado
    for j in jogadores:
        if j.nickname.lower() == nickname.lower():
            print(f"Já existe um jogador com o nickname '{nickname}'! Cadastro cancelado.")
            return

    turma = input("Turma: ").strip()
    jogador = Jogador(nome, nickname, turma)
    jogadores.append(jogador)
    print("Jogador cadastrado com sucesso!")


def cadastrarEquipe():
    print("\n--- Cadastrar Equipe ---")
    nome = input("Nome da equipe: ").strip()
    jogo = input("Jogo: ").strip()
    equipe = Equipe(nome, jogo)
    equipes.append(equipe)
    print("Equipe cadastrada com sucesso!")


def escolherJogador():
    if not jogadores:
        print("Nenhum jogador cadastrado ainda.")
        return None
    print("Jogadores cadastrados:")
    for i, j in enumerate(jogadores, 1):
        equipe_info = f" [Equipe: {j.equipe.nome}]" if j.equipe else ""
        print(f"  {i}. {j.nome} ({j.nickname}) - {j.turma}{equipe_info}")
    try:
        escolha = int(input("Escolha o número do jogador: "))
        if 1 <= escolha <= len(jogadores):
            return jogadores[escolha - 1]
        else:
            print("Número inválido.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None


def escolherEquipe():
    if not equipes:
        print("Nenhuma equipe cadastrada ainda.")
        return None
    print("Equipes cadastradas:")
    for i, e in enumerate(equipes, 1):
        print(f"  {i}. {e.nome} ({e.jogo})")
    try:
        escolha = int(input("Escolha o número da equipe: "))
        if 1 <= escolha <= len(equipes):
            return equipes[escolha - 1]
        else:
            print("Número inválido.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None


def adicionarJogador_equipe():
    print("\n--- Adicionar Jogador a uma Equipe ---")
    jogador = escolherJogador()
    if jogador is None:
        return
    equipe = escolherEquipe()
    if equipe is None:
        return
    sucesso = equipe.adicionarJogador(jogador)
    if sucesso:
        print("Jogador adicionado à equipe com sucesso!")


def listarEquipes():
    print("\n--- Lista de Equipes ---")
    if not equipes:
        print("Nenhuma equipe cadastrada ainda.")
        return
    for e in equipes:
        e.exibirResumo()


def listarJogadores_equipe():
    print("\n--- Jogadores da Equipe ---")
    equipe = escolherEquipe()
    if equipe is None:
        return
    equipe.exibirJogadores()


def buscarPorNickname():
    print("\n--- Buscar Jogador por Nickname ---")
    nick = input("Digite o nickname: ").strip()
    for j in jogadores:
        if j.nickname.lower() == nick.lower():
            print("  Jogador encontrado:")
            j.exibir()
            return
    print(f"  Nenhum jogador encontrado com o nickname '{nick}'.")


def removerJogador_equipe():
    print("\n--- Remover Jogador de uma Equipe ---")
    equipe = escolherEquipe()
    if equipe is None:
        return
    if not equipe.jogadores:
        print("  Esta equipe não possui jogadores.")
        return
    print(f"Jogadores de '{equipe.nome}':")
    for i, j in enumerate(equipe.jogadores, 1):
        print(f"  {i}. {j.nome} ({j.nickname}) - {j.turma}")
    try:
        escolha = int(input("Escolha o número do jogador a remover: "))
        if 1 <= escolha <= len(equipe.jogadores):
            jogador = equipe.jogadores[escolha - 1]
            equipe.removerJogador(jogador)
            print(f"  ✓ Jogador '{jogador.nickname}' removido da equipe '{equipe.nome}'!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida.")


# Loop principal
while True:
    exibirMenu()
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        cadastrarJogador()
    elif opcao == "2":
        cadastrarEquipe()
    elif opcao == "3":
        adicionarJogador_equipe()
    elif opcao == "4":
        listarEquipes()
    elif opcao == "5":
        listarJogadores_equipe()
    elif opcao == "6":
        buscarPorNickname()
    elif opcao == "7":
        removerJogador_equipe()
    elif opcao == "0":
        print("\nEncerrando o sistema. Até mais!")
        break
    else:
        print("Opção inválida! Digite um número do menu.")
