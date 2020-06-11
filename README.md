# Load Balancer

> Solving proposed problem for a load balancer.

***Proposed Problem description (pt-br)***

Balanceamento de carga é muito importante em ambientes Cloud. Estamos sempre tentando
minimizar os custos para que possamos manter o número de servidores o menor possível. Em
contrapartida a capacidade e performance aumenta quando adicionamos mais servidores.

Em nosso ambiente de simulação, em cada tick (unidade básica de tempo da simulação), os
usuários conectam aos servidores disponíveis e executam uma tarefa. Cada tarefa leva um
número de ticks para ser finalizada (o número de ticks de uma tarefa é representado por ttask ),
e após isso o usuário se desconecta automaticamente.

Os servidores são máquinas virtuais que se auto criam para acomodar novos usuários. Cada
servidor custa R$ 1,00 por tick e suporta no máximo umax usuários simultaneamente. Você
deve finalizar servidores que não estão sendo mais usados.

O desafio é fazer um programa em Python que recebe usuários e os aloca nos servidores
tentando manter o menor custo possível.

## How-to Run

***Help screen:***
```bash
python load_balancer.py --help
```

***Run:***
```bash
python load_balancer.py [input file] [output file] [base cost per tick per server]
```

## Example

***Input example (input.txt):***

- first line has the value for ttask (= 4);
- second line has the value for umax (= 2);
- the remaining lines contain the number of new users for each tick

```bash
4
2
1
3
0
1
0
1
```

***Output example (output.txt):***
```bash
1
2,2
2,2
2,2,1
1,2,1
2
2
1
1
0
15
```
