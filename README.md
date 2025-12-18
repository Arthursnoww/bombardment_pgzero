# 💣 BOMBARDMENT

**BOMBARDMENT** é um jogo de ação e estratégia inspirado no clássico Bomberman, desenvolvido em Python utilizando a biblioteca **Pygame Zero**.

## 🚀 Como Preparar o Ambiente (Linux)

Siga estes passos exatos para configurar o ambiente e rodar o jogo, assim como foi feito no desenvolvimento:

### 1. Atualize o sistema e instale o suporte a ambientes virtuais
Abra o terminal e execute:

    sudo apt update
    sudo apt install python3-venv
### 2. Criar e Ativar o Ambiente Virtual
Organize o projeto criando uma pasta dedicada e isolando as bibliotecas:
Bash

    mkdir meu_jogo_pgzero
    cd meu_jogo_pgzero
    python3 -m venv venv
    source venv/bin/activate

3. Instalar Dependências

Com o ambiente (venv) ativo, instale a biblioteca do jogo:
Bash

    pip install pgzero

4. Executar o Jogo

Certifique-se de que o arquivo bombardment.py e as pastas de mídia estão na raiz da pasta . Para jogar, execute:
Bash

      pgzrun bombardment.py

# 🎮 Como Jogar
## Objetivo

Sua missão é chegar ao Portal de Saída Azul no labirinto. Use bombas para abrir caminho destruindo os blocos e evite o contato com os monstros.

### Controles

Setas (⬆️⬇️⬅️➡️)	Mover o Mago

Barra de Espaço	Colocar Bomba

Tecla R	Reiniciar após Game Over ou Vitória
