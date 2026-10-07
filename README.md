# Mini S

Site do **Mini S**, projeto educacional e social das equipes de robótica da Escola SESI de Jaraguá do Sul. Reúne os 15 encontros (missões do robô Bolt) para que qualquer professor, como os das unidades do PIAL, baixe, imprima e aplique com a turma.

Feito com [Vue 3](https://vuejs.org/) + [Vite](https://vite.dev/), publicado de graça no GitHub Pages, com painel de administração [Sveltia CMS](https://github.com/sveltia/sveltia-cms) em `/admin`.

## Como funciona

```
content/            ← conteúdo do site (editado pelo painel /admin)
  aulas/*.json        uma ficha por aula
  equipes/*.json      uma ficha por equipe
  galeria.json        fotos dos encontros
  site.json           total de encontros, e-mail, apoiadores
public/
  admin/              painel da equipe (config.yml define os formulários)
  uploads/            PDFs e imagens enviados pelo painel
  pdf/, img/          material inicial
src/                ← código Vue (abas, componentes, estilos)
```

Quem publica aulas usa o painel. O passo a passo para a equipe está em **[TUTORIAL-PAINEL.md](TUTORIAL-PAINEL.md)**.

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
npm run dev
```

## Colocar no ar (uma vez)

1. O site fica na organização **`minis-sesi`**, no repositório público **`minis-sesi.github.io`**, branch `main`.
2. No repositório: **Settings → Pages → Source: GitHub Actions**.
3. O painel já aponta para `minis-sesi/minis-sesi.github.io` (`public/admin/config.yml`).
4. Em **Settings → Collaborators** (ou como membros da organização), adicione quem vai usar o painel.

A cada alteração (pelo painel ou por `git push`), o GitHub Actions publica o site em **https://minis-sesi.github.io**.
