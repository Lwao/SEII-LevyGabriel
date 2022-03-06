---
title:
- Trabalho final 1 - Simulação de um drone 2D
author:
- Levy G. S. Galvão
- Pedro H. S. F. Santos
language: pt-BR
numbersections: true
output:
    pdf_document:
        template: NULL
        toc: true
---

<!-- sudo apt-get install pandoc -->
<!-- pandoc report.md -o report.pdf -->

# Especificação do projeto

O presente trabalho, entitulado de projeto de simulação do drone ou projeto do drone, de forma curta, tem o objetivo de desenvolver uma simulação aplicando numericamente os conceitos físicos que envolvem a cinemática e dinâmica de um drone, ou qualquer *unmanned aerial vehicle* (UAV) com eixo de propulsão vertical. 

Também pretende-se implementar um sistema de controle de posição para que o drone ajuste suas variáveis internas com o objetivo de alcançar um destino especificado. 

A simulação deve ser feita por meio de um jogo 2D em linguagem `Python` e esta aplicação deve permitir que o drone seja movimentado pelas setas dos teclado, ou por meio do estabelecimento de pontos de destino que, após serem dispostos na tela da aplicação, o drone deverá definir sua trajetória para alcançar todos os pontos de acordo com a ordem estabelecida.

Para auxiliar o gerenciamento da simulação, a aplicação deve conter uma interface gráfica capaz de:

- Selecionar o modo em que a simulação irá operar, seja movimentando o drone por meio de setas no teclado ou por meio de pontos de destino estabelecidos por coordenadas cartesianas da tela ou pelo clique do mouse;
- Possuir botões para ativar o modo de depuração que permite observar os pontos de destino com clareza e destinção da ordem com que o drone irá perserguir, no caso do modo com pontos de destino e o mesmo conjunto de botões pode permitir observar o ponto de destino modificável pelas setas, no caso do modo de movimentação por setas no teclado;
- Ativar ou desativar painel com informações de depuração, e.g. taxa atual de frames, porcentagem de consumo da CPU, porcentagem de consumo da memória RAM;
- Permitir plots em tempo real da evolução das variáveis de estado e/ou exportação em um arquivo textual, e.g. `.csv` ou `.txt`.


# Módulos utilizados na aplicação

Para auxiliar o desenvolvimento da aplicação em `Python`, alguns módulos ou bibliotecas foram utilizados. A biblioteca `Pygame` foi utilizada no desenvolvimento das mecânicas do jogo. A biblioteca `Numpy` foi utlizada nos cálculos extensivos com vetores e demais operações algébricas que culminaram no funcionamento das simulações físicas e do sistema de controle. A biblioteca `Kivy` foi utilizada para fazer a interface gráfica entre homem e máquina que permitiu o gerenciamento da aplicação, incluindo seleção dos seus modos de operação e apresentação de informações do interesse do usuário.

# Integração do sistema

## Árvore de diretórios

Abaixo observa-se a árvore de diretórios que compõe o projeto do drone. Nela pode-se observar a divisão do aplicativo nos diretórios `/data`, `/gui_utils`, `/img` e `/sprites`, além do pasta raiz `/game`.

```
game
 |-- data
 | |- .gitignore
 | |- data.csv
 |-- gui_utils
 | |- Button.py
 | |- GUI.py
 |-- img
 | |- images...
 |-- sprites
 | |- Background.py
 | |- Drone.py
 | |- Waypoint.py
 |-- game.py
 |-- requirements.txt
```

De acordo com os diretórios, cada um guarda uma função específica:

- `/game` é o diretório raiz da aplicação e este contém todos os outros diretórios, o *script* principal de execução da simulação do drone e um arquivo de `requirements.txt` indicando as versões das bibliotecas em Python utilizadas para esta aplicação;
- `/sprites` contém as classes para as principais *sprites* utilizadas na simulação, estas são: `Background` para definir as telas de fundo do jogo e da interface com o usuário; `Waypoint` para definir a movimentação, colisão e visualização dos pontos de destino utilizados na simulação; e `Drone` contendo detalhes da cinemática e dinâmica do drone de acordo com as leis físicas e o sistema de controle interno de posição;
- `/img` contém todas as imagens utilizadas na aplicação, estas envolvendo plano de fundo, *sprites* e botões;
- `/gui_utils` contém as classes utilizadas para montar a interface gráfica interativa com o usuário, estas são: `Button` para gerar os botões e seu gerenciamento; e `GUI` que encompassa a totalidade dos botões utilizados na interface e demais gerenciamento da interface;
- `/data` é um diretório destinado a armazenar os arquivos `.csv` exportados pela aplicação e que contém dados relacionados às variáveis de estado do drone.

## Drone

## Interface gráfica com o usuário

A interface gráfica é dividida em duas classes apenas, a classe Button, que cria um objeto de botão, colocando as cores passadas, posicionamento, mudanças que podem acontecer no momento do clique, entre outras funções. Já a classe GUI tem uma função mais geral, utilizando a classe Button para criar seus vários botões e posicioná-los, com alguns labels para cada botão, sendo eles `mode`, `plot`, `analytics`, `csv`, `debug` e `power`. O botão `mode` serve par alterar o modo de jogo entre `joystick` e `waypoint`, o botão `plot` expõe as variáveis de estado do sistema do drone, enquanto o botão `csv` exporta-os para um arquivo `.csv`. O botão debug destaca o waypoint para se ter conhecimento em para onde o drone estará indo e o botão `analytics` plota na tela a performance do jogo na máquina. Por último, o botão `power` desliga a aplicação.
Dentro do jogo, depois que o objeto GUI é criado, sempre é verificado se algum label do botão foi alterado para atualizar as funções no jogo.

# Referências sobre conceitos extras
