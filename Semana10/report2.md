---
title:
- Tutorial sobre as ferramentas de toolchain para a compilação cruzada para sistemas embarcados
author:
- Levy G. S. Galvão
numbersections: true
output:
    pdf_document:
        template: NULL
---

<!-- sudo apt-get install pandoc -->
<!-- pandoc report.md -o report.pdf -->

Para a instalação de uma *toolchain* de interesse, os passos a seguir devem ser usados:

1. O primeiro passo é escolher a *toolchain* de interesse, levando em conta a presença da biblioteca C de interesse (comunicação com o kernel) e que seja fácil de atualizar. As *toolchains* pré compiladas constituem-se como uma fácil opção, apesar de serem menos flexível; as que devem ser compiladas completamente não são de fácil uso, porém mais flexível e possui amplo suporte da comunidade. Neste tutorial será utilizada a *toolchain* ["crosstool-NG"](http://crosstool-ng.github.io).

2. Em seguida o crosstool-NG deve ser instalado, iniciando pela clonagem do repositório e instalação da versão de interesse utilziando o `make`.

3. O passo seguinte é compilar a *toolchain* para o QEMU (emulador de processadores) e a partir do menu de configuração a opção *read-only* pode ser removida, assim permitindo a compilação.

4. O passo final é testar a *toolchain* ao compilar algum código fonte.

Considerando a instalação prévia da *toolchain*, os passos abaixo mostram a sequência de uso:

1. Analisar as configurações do compilador, tal como as opções de *target* e *host* da compilação, que se iguais constituem-se como uma compilação nativa, se não, uma compilação cruzada.
2. Analisar a biblioteca C, que possui as funções que servem de API para o kernel.
3. Utilizar vinculação estática estando ciente que o conteúdo de uma biblioteca estática existe fisicamente no arquivo executável a qual esta está vinculada, consequentemente aumentando o tamanho do executável; aumenta a velocidade de execução do programa, mas ao custo de uma compilação mais lenta;
4. Utilizar a vinculação dinâmica estando ciente que o processo de execução é realizado em tempo de execução, com as bibliotecas sendo carregadas em memória apenas uma vez; pode desencadear problemas de compatibilidade caso a biblioteca não seja recompilada; tempo de execução lento, mas com menores arquivos executáveis.