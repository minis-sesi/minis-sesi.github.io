# Mini S

Site do **Mini S**, projeto educacional e social das equipes de robótica da Escola SESI de Jaraguá do Sul. Reúne os 15 encontros (missões do robô Bolt) para que qualquer professor, como os das unidades do PEAL, baixe, imprima e aplique com a turma.

Feito com [Vue 3](https://vuejs.org/) + [Vite](https://vite.dev/), publicado de graça no GitHub Pages e sincronizado automaticamente com a pasta oficial do **Google Drive** do projeto.

## Como funciona

```
content/                  ← conteúdo do site (sincronizado com o Google Drive)
  aulas/*.json              uma ficha por aula
  equipes/*.json            uma ficha por equipe
  galeria.json              fotos dos encontros
  site.json                 total de encontros, e-mail, apoiadores
public/
  pdf/, img/paginas/        PDFs e páginas geradas automaticamente das aulas
  img/fotos/, uploads/      fotos dos encontros e logos de equipes/patrocinadores
scripts/
  sync_drive.py             robô que lê os PDFs e a planilha do Google Drive
src/                      ← código Vue (abas, componentes, estilos)
```

O passo a passo para publicar novas aulas pelo Google Drive está em **[TUTORIAL-PAINEL.md](TUTORIAL-PAINEL.md)**.

## Abas do site

| Aba | Arquivo |
| --- | --- |
| Início | `src/views/HomeView.vue` |
| Quem somos | `src/views/QuemSomosView.vue` |
| Sobre | `src/views/SobreView.vue` |
| Aulas (lista e página de cada aula) | `src/views/AulasView.vue`, `src/views/AulaView.vue` |
| Contatos | `src/views/ContatosView.vue` |

## Rodar no computador

```bash
npm install
npm run sync   # opcional: sincroniza novas aulas do Google Drive
npm run dev
```

## Publicação e Sincronização

1. O site fica na organização **`minis-sesi`**, no repositório público **`minis-sesi.github.io`**, branch `main`.
2. O workflow **Sincronizar Google Drive** (`.github/workflows/sync-drive.yml`) verifica o Drive automaticamente a cada 2 horas (ou manualmente via aba **Actions** do GitHub) e publica o site em **https://minis-sesi.github.io**.
