# Algoritmo de otimização do posicionamento de armadilhas para monitoramento da Diatraea saccharalis

<p align="center">
  <img src="images/interface.png" alt="interface do algoritmo"/>
</p>

Este repositório contém um algoritmo desenvolvido para otimizar o posicionamento das armadilhas utilizadas no monitoramento da **Diatraea saccharalis** (broca-da-cana) em plantações de cana-de-açúcar. O objetivo é maximizar a eficiência da cobertura dessas armadilhas.

Este algoritmo foi derivado de um projeto maior de gerenciamento geral de pragas da cana-de-açúcar chamado **Arapuca**, que está em desenvolvimento. Mais detalhes sobre esse sistema serão disponibilizados futuramente.

---

## Motivação

O monitoramento eficaz da **broca-da-cana** é um dos maiores desafios no manejo de pragas em extensas áreas agrícolas, como os canaviais. Esta praga pode causar danos significativos, afetando a produtividade e a qualidade da cana, tanto no campo quanto na indústria.

Tradicionalmente, o monitoramento dessa praga envolvia métodos manuais que podem são lentos e ineficientes, especialmente em áreas de grande extensão. De acordo com o engenheiro agrônomo **José Francisco Garcia**, diretor da **Global Cana – Soluções Entomológicas**, muitos campos na região Centro-Sul apresentam níveis alarmantes de infestação, e apenas um terço dos produtores adotam algum método de controle.

Garcia destaca que o uso de armadilhas para o monitoramento da broca-da-cana é uma ferramenta eficiente, simples e com alto rendimento. Cada armadilha cobre aproximadamente 50 hectares, e determinar sua localização ideal é crucial para otimizar o controle da praga. Um posicionamento estratégico pode reduzir em até 80% a penetração das lagartas nos colmos, se os produtos químicos forem aplicados no momento certo.

Este algoritmo tem como objetivo resolver o problema da distribuição espacial otimizada dessas armadilhas, garantindo uma cobertura ampla e eficiente para maximizar a detecção dos picos de infestação.

Resolvi separar este módulo do sistema **Arapuca** e disponibilizá-lo gratuitamente porque acredito que ele pode beneficiar os produtores de cana-de-açúcar, oferecendo uma ferramenta acessível, prática e facilmente adaptável às suas necessidades.

Referência: [A eficiência do uso de armadilhas no controle da broca-da-cana](https://www.canaonline.com.br/conteudo/a-eficiencia-do-uso-de-armadilhas-no-controle-da-broca-da-cana.html), publicado em **CanaOnline**.

---

## Solução

O algoritmo proposto utiliza as seguintes etapas para otimizar o posicionamento das armadilhas:

1. **Cálculo do número de armadilhas necessárias**: O algoritmo calcula o número necessário de armadilhas com base na área total dos talhões, assumindo que cada armadilha cobre 50 hectares.  
   - **Fórmula**: Número de armadilhas = Área total dos talhões (em ha) / 50 hectares.

2. **Geração de pontos potenciais**: O algoritmo cria pontos ao longo da borda dos talhões, onde cada ponto representa um possível local de instalação da armadilha.

3. **Criação de áreas de cobertura**: Para cada ponto gerado, o algoritmo cria um buffer de 50 hectares para representar a área de cobertura da armadilha.

4. **Intersecção com os talhões**: O algoritmo busca identificar as áreas de cobertura que têm maior interseção com os talhões.

5. **Atualização da área restante**: Após encontrar a melhor intersecção, a área de cobertura identificada é removida da área dos talhões.

6. **Iteração**: O processo é repetido até que o número necessário de armadilhas seja atingido, cobrindo a maior parte dos talhões de maneira eficiente.

### Resultado:

Após ao algoritmo ser executado teriamos uma saída parecida com essa, lembrando que essa não é uma fazenda real crie 
manualmente como exemplo, ela tem em torno de 2600 hectares, assim seria necessario 52 armadilhas.

<p align="center">
  <img src="images/points.png" alt="pontos de armadilhas" width="600"/>
</p>

---

## Como usar
### Requisitos:

- **QGIS**: Este algoritmo foi desenvolvido para ser utilizado com o software [QGIS](https://qgis.org), que oferece uma interface amigável e ferramentas avançadas para análise geoespacial.

### Como usar no QGIS:

Siga as instruções clicando [ [aqui](docs/setup.md) ].


## Próximos Passos

Algumas melhorias que planejo implementar incluem:

- **Otimização de performance**: Atualmente, o algoritmo é eficiente, mas acredito que há espaço para reduzir ainda mais o tempo de execução em áreas de grandes dimensões.

---

## Contribuições

Se você tiver sugestões, melhorias ou correções, sinta-se à vontade para abrir uma issue ou enviar um pull request.

---

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
