# Implementação-TLB

Este código simula o funcionamento de uma memória cache, com o preenchimento da tabela de endereços e contagem de HIT e MISS dos acessos à memória.

<h2> Configurações da TLB </h2>

- Cache de mapeamento associativo
- Algoritmo de substituição: LRU
- Códificação da CAM da TLB: Paridade Simples, Paridade no MSB, Paridade dos bits pares no MSB e paridade dos bits ímpares no MSB-1
- Inserção de estatística de falhas na memória

<h2> Alunos </h2>

- Milena Maia
- Walber Florêncio

<h2> Orientador </h2>

- Otávio Alcântara

<h2> Desenvolvimento </h2>

- [x] Preenchimento dos endereços
- [x] Algoritmo de substituição
- [x] Contagem de HIT e MISS
- [x] Contagem de Falsos Positivos
- [x] Mecanismo de injeção de falhas
- [ ] Teste com código de correção de erros
  - [x] MSB
  - [x] MSB-1
  - [ ] Proposta
- [ ] Teste com aplicação real
  - [x] cc1
  - [ ] AcroRead
  - [ ] Benchmark

<h2> Informação adicional </h2>

Código adaptado de Anselmo Battisti.
