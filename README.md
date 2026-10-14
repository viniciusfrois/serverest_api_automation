# ServeRest API Automation with GenAI

Projeto de automação REST.

## Stack e ferramenta GenAI

- Linguagem: Python 3.10+
- Automação: pytest + requests
- Assistente GenAI escolhido: ChatGPT, utilizado como assistente de código para estruturar fixtures, sugerir cenários, revisar assertions, refatorar o cliente HTTP e documentar a validação humana.
- API alvo: https://compassuol.serverest.dev/

## Escopo implementado

- Login: credenciais válidas, senha inválida e campos ausentes.
- Usuários: listagem, criação, e-mail duplicado e ID inexistente.
- Produtos: listagem, bloqueio sem autorização, criação e consulta com perfil administrativo e limpeza do produto temporário.
- Carrinhos: listagem, bloqueio sem autorização e produto inexistente.

A suíte possui 13 testes. Alguns cenários do plano original continuam como próximos passos: PUT/DELETE de usuários, edição de produtos, perfil comum tentando executar operações administrativas, estoque insuficiente, produto duplicado no carrinho, segundo carrinho, checkout/cancelamento e validação mais completa de payloads e limites.

## Configuração

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

O padrão de URL já aponta para a API alvo. Para trocar o ambiente, defina `BASE_URL`; para timeout, `REQUEST_TIMEOUT`.

## Execução e relatórios

```bash
pytest -v
pytest -v --junitxml=reports/junit.xml
```

O relatório JUnit é gerado pelo próprio pytest. Não execute em paralelo contra o ambiente compartilhado antes de validar isolamento e limpeza.

## Uso de GenAI

Prompt-base utilizado:

> Atue como QA Sênior de automação. Com base no plano de testes ServeRest, proponha e revise testes pytest para Login, Usuários, Produtos e Carrinhos. Cubra cenários positivos, negativos e edge cases. Use fixtures reutilizáveis, dados únicos, timeout e limpeza segura. Não invente endpoints ou regras: sinalize o que precisa ser confirmado no Swagger. Revise status HTTP, body e schema; explique cada mudança sugerida e não declare sucesso sem execução real.

A IA foi usada como apoio à estruturação da suíte, criação de fixtures, sugestões de cenários, revisão de asserts e documentação. As sugestões foram tratadas como propostas, não como verdade de contrato.

## Log de ajustes e validação humana

1. Centralização da URL base, timeout e métodos HTTP em um cliente reutilizável.
2. Criação de e-mails únicos para reduzir colisões no ambiente compartilhado.
3. Criação de fixtures para usuários comuns e administradores, incluindo obtenção de token.
4. Inclusão de limpeza best-effort para recursos temporários criados pelos testes.
5. Inclusão de asserts sobre status HTTP, campos principais e estrutura de listas.
6. Revisão crítica: status alternativos em alguns testes são tolerância provisória; devem ser fixados ao contrato documentado no Swagger antes da entrega final.
7. Execução neste ambiente de preparação: 13 testes foram coletados, mas a execução contra a API não pôde ser validada porque o ambiente de execução não conseguiu resolver o DNS de `compassuol.serverest.dev` (`Temporary failure in name resolution`). Portanto, não há evidência de aprovação funcional contra a API real.

## Repositório e artefato
Repositório público informado: https://github.com/viniciusfrois/serverest_api_automation. O repositório contém README,
testes, conftest.py, pytest.ini, requirements.txt, .env.example e pasta reports.
## Segurança e limitações

- Use apenas dados temporários e identificáveis de teste.
- O ambiente online pode ser compartilhado e alterado por terceiros.
- Não considere falha de conexão como defeito funcional da API.
- Não execute checkout ou operações destrutivas sem confirmar o impacto e os dados usados.
- Revise todos os cenários e resultados contra o Swagger oficial.
