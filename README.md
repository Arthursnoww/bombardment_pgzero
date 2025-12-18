# 💣 BOMBARDMENT

**BOMBARDMENT** é um jogo de ação e estratégia inspirado no clássico Bomberman, desenvolvido em Python utilizando a biblioteca **Pygame Zero**.

![Gameplay do BOMBARDMENT](Captura%20de%20tela%20de%202025-12-18%2000-31-26.png)

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


---

## 📜 Créditos

Este projeto foi construído com o apoio de artes e sons da comunidade open-source. Abaixo estão as devidas atribuições:

### 🎨 Artes e Imagens
* **Personagens e Lógica de Base:** Baseado no projeto Bomberman de [Forestf90](https://github.com/Forestf90/Bomberman).
* **Tileset do Labirinto:** [Tiny Dungeon](https://kenney.nl/assets/tiny-dungeon) por **Kenney.nl**.

### 🔊 Sons e Músicas
* **Música do Menu:** *"Cretaceous Dawn"* por **Kevin MacLeod** (incompetech.com). Licenciado sob [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/).
* **Música da Partida:** *"About to Log on"* por **fluffclipse**. Licenciado sob [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/).
* **Efeito de Game Over e Game Win:** [SFX](https://freesound.org/people/EVRetro/sounds/533034/) por **EVRetro** via Freesound.org.


