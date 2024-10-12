# Manual de Configuração e Uso

---

## Configurando o Projeto

Este projeto contém um algoritmo desenvolvido para ser executado como um script no **QGIS**, facilitando o posicionamento otimizado de armadilhas para o monitoramento da **Diatraea saccharalis**.

### Primeiros Passos:

1. Faça o download do projeto.
2. Abra o QGIS.

### Incluir o Script na Caixa de Ferramentas:

1. No QGIS, localize a **Caixa de Ferramentas** na parte lateral direita da interface.

<p align="center">
  <img src="../images/caixa_de_ferramenta.png" alt="Caixa de Ferramentas no QGIS"/>
</p>

2. Clique no ícone do **Python** localizado na parte superior da Caixa de Ferramentas. Um menu de opções será exibido.

<p align="center">
  <img src="../images/incluir_novo_script_na_caixa_de_ferramentas.png" alt="Menu Python no QGIS"/>
</p>

3. Selecione a opção **Adicionar Script à Caixa de Ferramentas** e procure o arquivo `diatraea_saccharalis_monitoring_trap_positioning_optimization_algorithm.py` nos arquivos do projeto.

<p align="center">
  <img src="../images/python.png" alt="Adicionar Script ao QGIS" width="800"/>
</p>

4. Acesse a seção **Scripts** da Caixa de Ferramentas (normalmente localizada na última opção). Dentro dela, você verá o grupo **cana-de-açúcar** e o script **Posição de Armadilhas para o Monitoramento da Diatraea saccharalis**.

<p align="center">
  <img src="../images/script_na_caixa_de_ferramenta.png" alt="Script Adicionado na Caixa de Ferramentas"/>
</p>

5. Ao clicar no script, a interface de execução será exibida.

<p align="center">
  <img src="../images/interface.png" alt="Interface de Execução do Script"/>
</p>

---

## Como Usar:

1. Com a interface do script aberta, selecione o polígono que representa a fazenda para a qual deseja calcular o posicionamento das armadilhas. Em seguida, clique em **Executar**.

<p align="center">
  <img src="../images/interface.png" alt="Seleção do Polígono para Execução"/>
</p>

2. Após a execução, os pontos das armadilhas otimizados serão exibidos, mostrando a maior área de cobertura para a fazenda.

<p align="center">
  <img src="../images/points.png" alt="Pontos de Armadilhas Otimizados" width="600"/>
</p>

---

Este manual guia você na configuração do script no QGIS e na utilização da ferramenta para otimizar o posicionamento das armadilhas na fazenda, garantindo maior eficiência na cobertura.
