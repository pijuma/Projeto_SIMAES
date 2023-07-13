# SIMAES <br> 

SIMAES (Sistema Inteligente de Monitoramento de Água por Emissão de Sinais), projeto realizado para a disciplina de Eletrônicapara Computação do curso de Ciência da Computação da USP - São Carlos <br>

# Motivação <br> 

A partir de um benchmarking realizado com uma dos grandes nomes das indústrias, Procter & Gamble, chegamos a um problema responsável por gerar diversas interrupções na linha de produção: **o gasto elevado para a medição de fluxo de água nas tubulações subterrâneas**, o que contribui com o desperdício de água industrial e reduz drasticamente o nível de produção, uma vez que, ocorrendo problemas de vazamento, não é possível encontrar o local com agilidade, demorando de 1 a 2 semanas para resolvê-lo. <br> 

Atualmente, como citado anteriormente, há uma solução disponível no mercado para resolver tal problema, contudo, tal opção, que utiliza cabeamento físico até os medidores, é extremamente cara, o que desmotiva as indústrias a utilizá-la. Tendo este problema em vista, nosso grupo visa oferecer uma solução eficiente e mais barata para ter um maior controle do fluxo de água em todas as seções das tubulações sem necessidade de cabeamento até cada local de medição, fazendo com que os vazamentos sejam localizados de forma muito mais rápida e certeira, poupando tempo, dinheiro e o desperdício de água - o elemento mais importante da vida humana.

# Componentes <br>

1. Sensor de fluxo de água via pulsos;

<img src="https://github.com/pijuma/Projeto_SIMAES/blob/main/seawatersensor.jpg" width="300" height = "300">

2. ESP32 LoRa WiFi;
   
<img src="https://github.com/pijuma/Projeto_SIMAES/blob/main/ESP32LoRa32V3.jpg" width="300" height="300">

3. FILTER PUMP MODEL 603 (Krystal Clear)
<br>

# Design <br> 

# Critical points do projeto

Pelo paraíso fiscal fornecido por alguns municípios para grandes indústrias, com o intuito de aumentar os empregos disponíveis da região, é comum que empresas se estabeleçam em um mesmo local com grandes campus, ou seja, com vários setores e linhas de produção para cada produto fornecido. Além da questão fiscal, essa estratégia diminui consideravelmente os gastos com transporte, de produtos e funcionários, e gastos com infraestrutura. Por outro lado, ao se criar um grande campus, cria-se a necessidade de se estabelecer extensas tubulações subterrâneas para cada linha de produção, um efeito cascata de falta de planejamento, visto que, em sua grande maioria, expansões de produção são necessárias repetidamente por alguma promoção online ou uma Black Friday, fazendo com que um problema em tubulações não planejadas se torne uma grande bola de neve, já que a manutenção delas é quase que inacessível.

Para exemplificar, imagine a visão aérea do bairro onde você mora. Nesse bairro, várias tubulações subterrâneas levam água potável para cada residência de sua rua e também levam o esgoto gerado para o tratamento mais próximo.

Digamos que a água que sai da empresa de saneamento de sua cidade só entra e sai (a água que sai é aquela que "não foi utilizada") por um local em cada bairro, ou seja, a quantidade de água que foi enviada para esse bairro tem que ser igual à soma de todas as águas consumidas por cada residência com a quantidade de água que saiu do bairro (quantidade de água enviada = quantidade de água consumida por cada residência + quantidade de água que sai).

Imagine agora que um certo dia essa conta não "bateu", ou seja, que a quantidade de água enviada não foi a mesma que a igualdade da equação. Poderíamos gastar horas discutindo sobre como os hidrômetros são imprecisos (o que poderia ser a causa mais lógica do problema), mas sendo este um cenário muito ideal, vamos desconsiderar esse caso.

A hipótese mais clara, então, é que em algum local, debaixo de todas as ruas de seu bairro, há um vazamento em alguma das tubulações. Então agora é com você, como vasos saber onde está o vazamento?

Bom, é basicamente esse o problema das grandes indústrias. Geralmente há poucas entradas e saídas para uma quantidade grande de "bairros", que são os setores de produção, com centenas de "casas", que são os maquinários que recebem toneladas de água 24 horas por dia e, por isso, quando há algum problema de vazamento, além de demorar muito tempo para descobrir que ele existe, o que gera um grande custo desnecessário, é necessário que se gaste várias semanas sem produzir para que perfurações no solo sejam feitas em vários locais até que o problema seja encontrado. 

Conquanto, mesmo que isso seja um problema para várias empresas, como citamos anteriormente, há uma solução para tal problema disponível para o mercado. Mas essa solução não chega sequer a ser imaginada, pois geraria um curso extraordinário para a instalação e manutenção do sistema, já que parte do princípio de levar cabeamento de energia e de internet para cada ponto que se quer monitorar, ou seja, teriamos que reconstruir toda a infraestrutura de rede e de energia para criar centenas de pontos de conexões com cabos que chegariam a mais de 3 km para ter um sistema de monitoramento de tubulações (que possivelmente vai precisar de outro sistema para monitorar esses mesmos cabeamentos caso eles estejam com problemas, o que gera mas uns vez um problema em cascata).

# Resolvendo os critical points do projeto
Em suma, os principais pontos que o nosso sistema tem que abranger são:

   - Obter, de forma barata, centenas de medições realizadas por hidrômetros subterrâneos estrategicamente distribuídos sem a utilização de cabeamento físico de internet e de energia;
   - Obter um sistema que informe automaticamente quando um vazamento começou e de forma aproximada onde o problema de vazamento está para que action plans possam ser criadas com rapidez e precisão, com o fito de evitar o gasto desnecessário de água e a parada de produção.

Para atingir esses objetivos, depois de longas pesquisas è benchmarkings com donos de tecnologias industriais, montamos a seguinte schematic:
Para a conexão entre o hidrômetro subterrâneo e a central que deverá receber todos os dados em tempo real utilizamos dois microcontroladores ESP32 LoRa WiFi, que tem um baixo custo de energia e de aquisição, um sendo o transmissor e o outro o receptor. O transmissor, que terá um código identificador único, recebe os pulsos elétricos do sensor de água (hidrômetro) por meio de um pino análogico, armazena esse pulso na memória local e a cada um segundo envia, através da tecnologia LORa (Long Range) (método de comunicação por rádio frequência), a quantidade de pulsos que passaram nessa quantidade de tempo em conjunto com o seu código único, que servirá para identificar o local que enviou esse dado, para o receptor central. Já o receptor central, após cada dado recebido dos transmissores, repassa esses dados para o nosso servidor hospedado localmente utilizamos o framework Flask) via requisição socket.

Chegando ao fim do ciclo da troca de informações entre os sistemas, o nosso servidor local irá processar esses dados e armazenar cada dado recebido e nossa database com as informações de data e hora que o dado foi recebido, qual foi o endereço ip que enviou e identificador único do transmissor (que servirá para sabermos de onde o dado veio. Essas informações do fluxo de água são armazenados em um site, que pode ser acessado por qualquer dispositivo conectado a essa rede Wi-Fi.


# Comunicação <br> 

**LoRa-Rasps**  


**Wifi-Rasp-ESP receptor** 

# Site <br> 

Foi criado um site que tem como objetivo pedir dados de pulso, data e horário via HTTPS, e mostrá-los de forma gráfica. Para tanto, o site mostra onde o circuito estará localizado de acordo com o a planta do ICMC e apresenta as informações como o fluxo de água, passando a quantidade de pulsos. 

Foram implementados 2 métodos diferentes: O que pega o último dado guardado no servidor, calcula a quantidade de vazão em litros por segundos para aquele momento e mostra tanto no display localizado na planta do ICMC, quanto na coluna de dados à esquerda da imagem, de forma contínua. Tal display pode ser movimentado de acordo com o local que foi medido o fluxo de água. O outro método consiste na especificação do dia e do intervalo de horários que se quer analisar, para visualizar os dados em um período mais amplo. Essa visualização é possível por meio da coluna que mostrará os dados por minutos (para não mostrar dados demais, pois os dados são recebidos a cada segundo), e por meio da quantidade de litros totais que se passam no dado intervalo de tempo.

# Metodologia <br>

- Elaboração do roteiro e viabilidade do projeto;
- Desenho do projeto no papel;
- Compra e teste dos elementos;
- Montagem do sistema de fluxo de água para teste do protótipo;
- Teste de sinais em diversos fluxos e vazões de água;
