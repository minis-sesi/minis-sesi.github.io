# Tutorial: como publicar aulas no site do Mini S

Existem **duas formas** de publicar aulas no site:
1. **🏆 Pelo Google Drive + Planilha (Recomendado — sem precisar de senha ou conta no GitHub!)**
2. **🔒 Pelo Painel `/admin` (Opcional — para editar fotos, apoiadores e configurações)**

---

## 🏆 Opção 1: Publicar pelo Google Drive (Sem Login)

O site é sincronizado automaticamente com a pasta compartilhada do **Google Drive do Mini S**:
👉 **<https://drive.google.com/drive/folders/1TeA6AENeQ5RrVho9R6CdlckK_InAXTpp?usp=sharing>**

### Passo 1: Colocar o PDF na pasta da aula
1. Abra a pasta **`Atividades e Planos de Aula`** no Google Drive.
2. Entre na pasta correspondente ao encontro (ex.: `Aula 09_FRC`, `Aula 12_FRC`, `Aula 13_STEM RACING`...).
3. Envie o arquivo **PDF final da aula** lá dentro.

### Passo 2: Preencher os detalhes na Planilha (Opcional, mas recomendado)
Para personalizar o título, resumo, objetivos, materiais e vídeo do YouTube sem mexer em código:
1. Suba o arquivo **`PLANILHA-AULAS-DRIVE.csv`** (que está neste repositório) para a pasta do Google Drive.
2. Clique com o botão direito nele no Drive → **Abrir com → Planilhas Google (Google Sheets)** e salve como Planilha Google (`Arquivo → Salvar como Planilhas Google`).
3. Preencha ou edite a linha da aula (separando itens de listas como *Habilidades*, *Objetivos*, *Roteiro* e *Materiais* por `;`).

### Passo 3: Atualização automática do site
- O robô do site verifica o Google Drive automaticamente **a cada 2 horas** (ou imediatamente quando acionado na aba **Actions → Sincronizar Google Drive** do GitHub).
- Ele baixa o PDF novo, **gera sozinho a imagem de capa e todas as páginas em alta definição** e publica a aula no site!

---

## 🔒 Opção 2: Usar o Painel `/admin` (Para fotos, equipes e patrocinadores)

Endereço do painel: **`https://minis-sesi.github.io/admin/`**
(também tem o link **🔒 Área da equipe** no rodapé do site)

> 💡 **Novidade:** Se você publicar uma aula pelo `/admin` enviando apenas o **PDF**, o servidor agora gera a **capa e as imagens das páginas automaticamente** durante a publicação!

### 1. Preparar o acesso ao `/admin` (só uma vez)
1. Acesse <https://github.com/signup> e crie uma conta.
2. Envie o seu **nome de usuário do GitHub** para o responsável do repositório e aceite o convite por e-mail.
3. Acesse <https://github.com/settings/tokens/new> e preencha:
   - **Note** (nome): `Painel Mini S`
   - **Expiration** (validade): `Custom` → escolha uma data daqui a 1 ano
   - **Select scopes** (permissões): marque **somente** `public_repo`
4. Clique em **Generate token** e copie o código que começa com `ghp_`.

### 2. Entrar no painel
1. Abra `https://minis-sesi.github.io/admin/`.
2. Clique em **Entrar Usando Token de Acesso** e cole o seu token (`ghp_...`).

### 3. Adicionar fotos dos encontros ou patrocinadores
- **Galeria de fotos:** clique em **Site → Galeria de fotos** → **Adicionar Foto** → Salvar.
- **Equipes e Apoiadores:** clique em **Equipes** ou **Site → Configurações gerais** → Salvar.
