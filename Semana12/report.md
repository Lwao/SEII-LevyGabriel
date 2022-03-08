---
title:
- Atualização Over-the-Air (OTA)
author:
- Levy G. S. Galvão
numbersections: true
output:
    pdf_document:
        template: NULL
---

<!-- sudo apt-get install pandoc -->
<!-- pandoc report.md -o report.pdf -->

# O que é o serviço de atualização Over-the-Air (OTA)

O serviço de atualização Over-the-Air (OTA) permite a atualização contínua do software de um dispositivo lançado em produção sem a necessidade que um operador atue manualmente na manutenção. Como o próprio nome sugere, essa atualização é feita pelo ar, configurando-se como uma atualização à distância, permitindo escalar a taxa de atualização de produtos, uma vez que não há necessidade de contato por fio para atualização do novos pacotes.

# Qual o cenário onde esse sistema pode ser aplicado?

A atualização via OTA está presente nos mais diversos dispositivos que possuem conexão com rede sem fio e, considerando a era dos dispostivios IoT, estes são uma maioria.

Como exemplo de dispotivos, pode-se considerar a atualização do firmware de microcontroladores com tarefas específicas na indústria; mas também automóveis inteligentes que ao longo do tempo desenvolveram cada vez mais funções que dependem de software; smartwatches, smartphones e wearable tech em geral; dispostivos de propósito geral como computadores e notebooks também podem passar por essa atualização, apesar de também possuirem conexão cabeada via Ethernet.

O cenário principal de interesse do uso da atualização OTA é para casos que o dispositivo está localizado em locais remotos (sensores IoT) ou que possuam um terminal de difícil acesso pelo usuário (carros autônomos).

# Qual a diferença entre FOTA e SOTA?

Software-over-the-air (SOTA) é um conceito mais generalista que aborda o donwload de componentes de software para atualização de qualquer sistema ou dispositivo, enquanto que o firmware-over-the-air (FOTA) é uma atualização mais específica voltado ao campo do firmware, comportando desde a atualização de um patch para uma imagem existente de firmware ou até um imagem completamente nova.

# Desenhe uma arquitetura de atualização de software para uma empresa de carros autônomos considerando o hardware/software embarcado e o sistema de cloud para fornecer a atualização

Considerando a situação problema, permite-se traçar uma arquitetura que possui vários nós em produção correspondentes aos carros autônomos e que estão conectados à cloud por meio de uma rede de comunicação sem fio. 

Do outro lado da nuvem estão conectados os desenvolvedores e toda a cadeia de gerenciamento e lançamentos dos pacotes de atualização, que por meio de suas ferramentas de desenvolvimento lançam as atualizações para o hardware/software de cada carro de forma centralizada pela nuvem.

A figura abaixo ilustra a arquitetura.

<center> Figura 1 - Exemplo de arquitetura para atualização OTA.

[](ota.jpg)

</center>