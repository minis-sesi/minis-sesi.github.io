# Tutorial: como publicar aulas no site do Mini S

O site tem um **painel da equipe** onde dá para publicar aulas (PDF), fotos e editar as equipes sem mexer em código.
Depois de salvar, o site se atualiza sozinho em cerca de **2 minutos**.

Endereço do painel: **`https://minis-sesi.github.io/admin/`**
(também tem o link **🔒 Área da equipe** no rodapé do site)

---

## Parte 1: Preparar o acesso (só uma vez)

### 1.1 Criar a conta no GitHub
1. Acesse <https://github.com/signup> e crie uma conta (pode ser com o e-mail da escola).
2. Envie o seu **nome de usuário do GitHub** para o André.
3. Você vai receber um **convite por e-mail** para o repositório do Mini S. Clique em **Accept invitation**.

### 1.2 Criar a sua "chave de acesso" (token)
O token funciona como a senha do painel. Ele é criado uma vez e vale por 1 ano.

1. Entre no GitHub e acesse: <https://github.com/settings/tokens/new>
2. Preencha:
   - **Note** (nome): `Painel Mini S`
   - **Expiration** (validade): `Custom` → escolha uma data daqui a 1 ano
   - **Select scopes** (permissões): marque **somente** `public_repo`
3. Clique em **Generate token** no fim da página.
4. **Copie o código que começa com `ghp_`** e guarde num lugar seguro (por exemplo, o gerenciador de senhas do navegador).
   O GitHub só mostra esse código uma vez.

> ⚠️ Não envie o token por WhatsApp ou e-mail e não compartilhe com ninguém. Se perder, é só criar outro (passo 1.2 de novo).

---

## Parte 2: Entrar no painel

1. Abra o endereço do painel.
2. Clique em **Entrar Usando Token de Acesso**.
3. Cole o seu token (`ghp_...`) e confirme.

Na próxima vez o navegador já lembra o login.

---

## Parte 3: Publicar uma aula nova

1. No menu da esquerda, clique em **Aulas**.
2. Clique em **Novo** (ou **Nova Aula**).
3. Preencha os campos:

| Campo | O que colocar | Obrigatório |
| --- | --- | --- |
| **Número da aula** | A posição na trilha (1 a 15) | ✅ |
| **Título** | Ex.: *Os Projetos Perdidos* | ✅ |
| **Equipe que criou** | Escolha na lista | |
| **PDF da aula** | Clique e envie o PDF | ✅ |
| **Resumo** | 2 ou 3 frases sobre a aula | ✅ |
| Série, módulo, idade, tempo | Como aparece na capa do material | |
| Habilidades, objetivos, roteiro, materiais | Ajuda o professor a se preparar | |
| Imagem de capa / imagens das páginas | **Pode deixar vazio**: o site gera a prévia a partir do PDF | |
| Vídeo no YouTube | Cole o link do vídeo (pode ser "não listado") | |

4. Clique em **Salvar** (no topo).
5. Espere cerca de 2 minutos e atualize o site: a aula aparece no lugar do "Em breve" daquele número.

**Para corrigir uma aula:** Aulas → clique na aula → altere → Salvar.
**Para esconder uma aula sem apagar:** desmarque **Mostrar no site**.

---

## Parte 4: Adicionar fotos dos encontros

1. No menu, clique em **Site** → **Galeria de fotos**.
2. Clique em **Adicionar Foto**, envie a imagem e escreva uma legenda curta.
3. Salvar.

As 6 primeiras fotos aparecem na página inicial e todas aparecem em **Quem somos**.

> 📸 Antes de publicar fotos de crianças, confirme que existe autorização de uso de imagem dos responsáveis.

---

## Parte 5: Equipes, apoiadores e outras configurações

- **Equipes**: nome, categoria, descrição, Instagram e logo de cada equipe. Para incluir a 4ª equipe: Equipes → Novo.
- **Site → Configurações gerais**: total de encontros planejados (hoje 15), e-mail de contato, PDF com todo o material e parceiros/apoiadores (com logo).

---

## Dicas

- **Tamanho dos arquivos:** prefira PDFs com até ~20 MB. Se ficar maior, comprima em <https://www.ilovepdf.com/pt/comprimir_pdf>.
- **Fotos:** JPG de até ~1 MB carregam rápido no celular.
- **Errou algo?** Nada se perde: todo salvamento fica registrado no histórico do GitHub e pode ser desfeito pelo André.
- **O site não atualizou?** Espere mais um pouco e recarregue a página com `Ctrl + F5`.
