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

# Referências sobre conceitos extras
