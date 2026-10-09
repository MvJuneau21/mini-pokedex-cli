# RESPOSTAS.md — Mini-Pokédex CLI

Aluno: Marcus Vinícius Junho
Projeto: Mini-Pokédex CLI (PokéAPI + Python)

---

## 1. Escolha do modelo em cada etapa

| Etapa | Modelo | Por quê |
|---|---|---|
| Planejamento (plan mode, plan.md, CLAUDE.md) | Opus | Decisões que afetam o projeto inteiro: escolha da API, escopo, dependências, divisão das etapas. |
| Execução (código, testes) | Sonnet | Com o plano pronto, a tarefa é bem definida. O Sonnet escreve bem, é mais rápido e mais barato. |
| Revisão | Opus | Achar bugs e casos de erro que passaram batido exige raciocínio mais profundo. |
| Tarefas simples (README, ajustes pequenos) | Haiku | Texto e mudanças pequenas não precisam de um modelo caro. |

Eu usaria o modelo mais forte nos dois momentos em que pensar bem é mais importante do que escrever rápido: o planejamento e a revisão. No planejamento, um erro de decisão (por exemplo, escolher uma API ruim ou um escopo grande demais) contamina todas as etapas seguintes, então vale pagar mais por um raciocínio melhor. Na revisão, o desafio é encontrar problemas que não são óbvios, como o que acontece quando a internet cai ou o Pokémon não existe, e isso também pede mais capacidade.

Na execução, o plano já está aprovado e as tarefas são claras (como "faça uma função que chama a API e trata o erro 404"). Aqui o Sonnet resolve bem, com custo e tempo menores. Ter um plano detalhado é justamente o que permite usar um modelo mais barato sem perder qualidade.

Para o README e pequenos ajustes, o Haiku basta: são tarefas simples, em que velocidade e custo importam mais que profundidade.

A regra que usei foi: quanto mais difícil é desfazer ou perceber um erro, mais forte deve ser o modelo.

---

## 2. Quando usar `/clear` e `/compact`

O que cada um faz:

- `/compact` resume a conversa até aqui e continua com esse resumo. Libera espaço na janela de contexto, mas mantém o fio do que estava sendo feito.
- `/clear` apaga todo o histórico da conversa e começa do zero. Os arquivos do projeto e o CLAUDE.md continuam, então o Claude os relê e se reorienta.

Em que momentos do desenvolvimento eu usaria cada um, e por quê:

| Momento do projeto | Comando | Por quê |
|---|---|---|
| Depois de terminar o cliente da API e o CLI (etapas 2 e 3), com a conversa já longa | `/compact` | Ainda preciso do contexto (decisões, nomes de funções, erros já corrigidos) para escrever os testes, mas não de todo o histórico detalhado. |
| Antes da revisão (etapa 5) | `/clear` | Quero um revisor "de cara limpa", sem o histórico de quem escreveu o código. Ele relê o CLAUDE.md, o plan.md e o código, e vê os problemas sem viés. |
| Ao trocar de assunto (ex.: sair do código e ir escrever o README) | `/clear` | O contexto antigo não ajuda mais e só gasta espaço. |

A janela de contexto é limitada. Quando ela enche, o Claude pode perder detalhes do começo da conversa, ficar mais lento e mais caro, e começar a errar ou esquecer regras. Por isso o CLAUDE.md e o plan.md são importantes: guardam o que precisa sobreviver ao `/clear`. A regra prática é: `/compact` quando ainda preciso do fio da conversa, `/clear` quando quero recomeçar com a cabeça limpa.

---

## 3. O que poderia dar errado sem o plan mode

1. Decisões tomadas sem eu perceber. Sem plano, o Claude poderia escolher sozinho usar a biblioteca `requests` (que precisa de `pip install`), ou outra API, ou outra linguagem. Eu só descobriria quando o projeto não rodasse na minha máquina ou no computador do professor.
2. Escopo crescendo e arquivos demais. Eu pedi um mini-projeto, mas sem um limite combinado o Claude poderia adicionar cache em disco, interface gráfica, evoluções, imagens... Mais código para eu entender, mais chance de bug e menos controle. No plano, o escopo ficou fechado em 3 comandos.
3. Construir a coisa errada e só perceber no fim. Se eu deixasse tudo rodar sozinho, poderia receber 300 linhas de código no final que não são o que eu queria. Corrigir depois custa mais tempo e mais tokens do que ajustar o plano antes.
4. Perder a compreensão do que foi feito. Sem aprovar etapa por etapa, eu não saberia explicar o código. O plan mode me força a ler e entender antes de executar.

---

## 4. Diário do projeto

| Etapa | Modelo que usei | O que aconteceu / o que corrigi / o que aprendi |
|---|---|---|
| 1. Estrutura e docs | Opus | Entrei em plan mode, escolhi PokéAPI + Python CLI só com biblioteca padrão e aprovei o plano antes de qualquer arquivo ser criado. Gerou plan.md e CLAUDE.md. |
| 2. Cliente da API | Sonnet | Troquei para Sonnet com `/model sonnet`. Testei com a API real (Pikachu = id 25) e com erros (nome inexistente, entrada vazia). Ao revisar, vi que o 404 era detectado comparando texto da mensagem, o que é frágil, e troquei por uma exceção própria (`NaoEncontrado`). Aprendi que a ordem dos `except` importa: `HTTPError` vem antes de `URLError`. |
| 3. CLI | Sonnet | Funcionou com dados reais nos 3 comandos (`info`, `tipo`, `comparar`) e nos casos de erro (Pokémon inexistente e `--limite 0` mostram uma mensagem curta e saem com código 1). Aprendi que separar as funções que formatam das que buscam dados deixa o código testável sem internet. |
| 4. Testes | Sonnet | 15 testes passando offline, com mock da rede. Testei o caminho feliz, o 404, a queda de internet, o cache e o código de saída do `main`. Aprendi que mock deixa o teste rápido e independente da API. |
| 5. Revisão | Opus | Dei `/clear` antes para revisar "de cara limpa". Os 15 testes passavam e os comandos funcionavam, mas a revisão achou 4 problemas: timeout de conexão mostrava "verifique sua internet" (o Python embrulha o timeout dentro de `URLError`); conexão caindo no meio da resposta e Ctrl+C mostravam traceback; mensagens de erro misturavam inglês ("em type", "um(a) pokemon"). Corrigi e acrescentei 4 testes (19 no total). Aprendi que testes passando não garantem que todos os casos de erro foram pensados. |
| 6. README | Haiku | Criei o README com requisitos, os três comandos com exemplos, a seção de erros (exit code 1), como rodar os testes e uma tabela com a função de cada arquivo. Antes de dar a etapa por concluída, rodei os exemplos: `info "mr mime"` funciona, e `info mr mime` sem aspas dá erro, como o README avisa. Aprendi que um README só é confiável quando os comandos dele foram rodados de verdade. |

Usei `/compact`? Não usei.

Usei `/clear`? Antes da Etapa 5 (revisão), para o revisor não carregar o histórico de quem escreveu o código.

---

## 5. O que eu entendi do código

- Por que só a biblioteca padrão: o projeto precisa rodar em qualquer computador com Python 3.10+, sem `pip install`. `urllib` e `json` já vêm com o Python, então fazer a requisição HTTP não exige nenhuma dependência extra. Usar `requests` obrigaria quem for testar a instalar um pacote antes de rodar.
- Por que os testes usam mock: os testes trocam a chamada à rede (`pokeapi.get_json`, ou `urlopen`) por uma resposta fixa. Assim eles rodam sem internet, são rápidos e não quebram se a API cair ou um dado mudar. Também permite testar erros difíceis de provocar de verdade, como a queda de conexão e o timeout.
- O que acontece quando o Pokémon não existe: a PokéAPI devolve 404, e `get_json` lança `NaoEncontrado`. Em seguida, `_buscar` troca a mensagem por "Pokémon não encontrado: 'x'.". Por fim, o `main` captura o erro, imprime "Erro: ..." no stderr e retorna exit code 1, sem traceback.
