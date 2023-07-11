# SIMAES <br> 

SIMAES (Sistema Inteligente de Monitoramento de Água por Emissão de Sinais), projeto realizado para a disciplina de Eletrônica do curso de Ciência da Computação da USP - São Carlos <br>

# Motivação <br> 

A partir de um benchmarking realizado com uma dos grandes nomes das indústrias, Procter & Gamble, chegamos a um problema responsável por gerar diversas interrupções na linha de produção: **o gasto elevado para a medição de fluxo de água nas tubulações subterrâneas**, o que contribui com o desperdício de água industrial e reduz drasticamente o nível de produção, uma vez que, ocorrendo problemas de vazamento, não é possível encontrar o local com agilidade, demorando de 1 a 2 semanas para resolvê-lo. <br> 

Atualmente, como citado anteriormente, há uma solução disponível no mercado para resolver tal problema, contudo, tal opção, que utiliza cabeamento físico até os medidores, é extremamente cara, o que desmotiva as indústrias a utilizá-la. Tendo este problema em vista, nosso grupo visa oferecer uma solução eficiente e mais barata para ter um maior controle do fluxo de água em todas as seções das tubulações sem necessidade de cabeamento até cada local de medição, fazendo com que os vazamentos sejam localizados de forma muito mais rápida e certeira, poupando tempo, dinheiro e o desperdício de água - o elemento mais importante da vida humana.

# Componentes <br>

1. Sensor de fluxo de água via pulsos;

<img src="https://github.com/pijuma/Projeto_SIMAES/blob/main/sensor.jpg" width="300" height = "400">

2. Raspberry Pi 3 Versão 1.2 modelo D;
3. ESP32 LoRa WiFi;
   
<img src="https://github.com/pijuma/Projeto_SIMAES/blob/main/ESP32LoRa32V3.jpg" width="300" height="300">

5. FILTER PUMP MODEL 603 (Krystal Clear)
<br>

# Design <br> 

# Resumo
Foram utilizados dois microcontroladores ESP32 LoRa WiFi, um sendo o transmissor e o outro o receptor, e um micro-computador de placa única Raspberry Pi 3. O transmissor recebe os sinais do sensor de água através da tecnologia LoRa (Long Range), um método de comunicação por rádio frequência. Após conectar os microcontroladores em uma rede WiFi, o ESP32 transmissor passa os dados para o receptor através do WiFi. Conetando também o Raspberry, é possível transferir os dados do receptor para ele através de um protocolo de comunicação entre dispositivos MQTT (Message Queuing Telemetry Transport). Para conectar a Raspberry a um computador, é utilizado o protocolo de rede SSH (Secure Shell), que permite gerenciar os dados de forma remota. Essas informações do fluxo de água são armazenadas em um site, que pode ser acessado por qualquer dispositivo concetado a essa rede Wi-Fi.

# Comunicação <br> 

**LoRa-Rasps**  


**Wifi-Rasp-ESP receptor** 

# Site <br> 

Fizemos a montagem de um site que mostra onde o circuito estará localizado de acordo com o a planta do ICMC e apresentará as informações como o fluxo de água, passando a quantidade de pulsos. 

# Metodologia <br>

- Elaboração do roteiro e viabilidade do projeto;
- Desenho do projeto no papel;
- Compra e teste dos elementos;
- Montagem do sistema de fluxo de água para teste do protótipo;
- Teste de sinais em diversos fluxos e vazões de água;
