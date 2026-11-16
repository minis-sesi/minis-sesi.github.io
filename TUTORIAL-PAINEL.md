# Tutorial: como publicar aulas no site do Mini S pelo Google Drive

O site do **Mini S** (<https://minis-sesi.github.io/>) é sincronizado diretamente com a pasta compartilhada do **Google Drive**.
As equipes **não precisam mexer em código nem criar chaves de acesso**: basta colocar o PDF na pasta da aula no Google Drive!

---

## 📂 Parte 1: Onde colocar os arquivos no Google Drive

Acesse a pasta oficial do projeto no Google Drive:
👉 **<https://drive.google.com/drive/folders/1TeA6AENeQ5RrVho9R6CdlckK_InAXTpp?usp=sharing>**

Dentro dela, abra a pasta **`Atividades e Planos de Aula`**.

### 1.1 Publicar uma aula da trilha (Aulas 01 a 15)
1. Abra a pasta correspondente à aula (por exemplo: `Aula 09_FRC`, `Aula 12_FRC`, `Aula 13_STEM RACING`, `Aula 14_STEM RACING` ou `Aula 15_ S ROBOTS e S ATLAS`).
2. **Envie o arquivo PDF final da aula** para dentro dessa pasta.
3. Pronto! O sistema vai identificar o PDF automaticamente, gerar a imagem de capa, converter todas as páginas para visualização no site e liberar o botão de download.

### 1.2 Criar uma aula nova além das 15 (ex.: Aula 16, Aula 17...)
Se quiserem adicionar novos encontros:
1. Dentro de **`Atividades e Planos de Aula`**, clique em **Novo → Nova pasta**.
2. Nomeie a pasta seguindo o padrão **`Aula XX_EQUIPE`**:
   - `Aula 16_FTC` *(atribui automaticamente à equipe S ROBOTS FTC)*
   - `Aula 16_FRC` *(atribui automaticamente à equipe S ROBOTS FRC)*
   - `Aula 16_STEM RACING` *(atribui automaticamente à equipe Scuderia S ATLAS)*
3. Coloque o **PDF da aula** dentro dessa nova pasta.

---

## 📊 Parte 2: Personalizar textos da aula pela Planilha do Drive (Opcional)

Se você colocar apenas o PDF na pasta, o robô já descobre o título, a equipe e um resumo básico sozinho.
Mas, se quiser personalizar **título, resumo, série, módulo, idade recomendada, tempo estimado, habilidades, objetivos, roteiro, materiais ou vídeo do YouTube**:

1. Na pasta do Google Drive, abra a planilha de aulas (você pode enviar o arquivo modelo **`PLANILHA-AULAS-DRIVE.csv`** para o Drive e clicar em **Abrir com → Planilhas Google → Arquivo → Salvar como Planilhas Google**).
2. Edite a linha correspondente ao **Número** da aula:

| Coluna | O que preencher | Exemplo |
| --- | --- | --- |
| **Numero** | Número da aula na trilha | `9` |
| **Titulo** | Nome da missão ou oficina | `O Mundo da FRC` |
| **Equipe** | Equipe responsável | `S ROBOTS FRC`, `S ROBOTS FTC` ou `Scuderia S ATLAS` |
| **Serie** | Série ou categoria | `FIRST Robotics Competition`, `S Robots Explorer`, `STEM Racing` |
| **Modulo** | Tema do módulo | `Tecnologia FRC` |
| **Resumo** | 2 ou 3 frases sobre a atividade | `As crianças conhecem como funciona um robô industrial...` |
| **Idade** | Faixa etária | `6 a 12 anos` |
| **Tempo** | Duração da aula | `30 a 45 min` |
| **Habilidades** | Separadas por ponto e vírgula (`;`) | `Criatividade; Trabalho em equipe; Raciocínio lógico` |
| **Objetivos** | Separados por ponto e vírgula (`;`) | `Conhecer os sistemas do robô; Trabalhar em dupla` |
| **Roteiro** | Passo a passo separado por `;` | `Etapa 1: Apresentação; Etapa 2: Desafio prático` |
| **Materiais** | Lista de materiais separada por `;` | `Atividade impressa; Lápis de cor; Tesoura sem ponta` |
| **Video** | Link do vídeo no YouTube (opcional) | `https://youtu.be/...` |

---

## 🔄 Parte 3: Como o site se atualiza

Existem **duas formas** de o site puxar as novidades do Google Drive:

### 1. Automática (sem fazer nada)
- De **2 em 2 horas**, o robô do GitHub verifica o Google Drive sozinho e publica qualquer aula nova que encontrar.

### 2. Atualização imediata (em 1 minuto)
Se você acabou de subir um PDF no Google Drive e quer ver no site na mesma hora:
1. Entre na sua conta do GitHub e acesse a aba **Actions** do repositório:
   👉 **<https://github.com/minis-sesi/minis-sesi.github.io/actions>**
2. Você pode fazer de dois jeitos:
   - **Jeito A (Sincronizar e salvar no repositório):** No menu da esquerda, clique em **`Sincronizar Google Drive`** → clique no botão **`Run workflow`** (na direita) → botão verde **`Run workflow`**.
   - **Jeito B (Reexecutar publicação):** Clique na última execução de **`Publicar site`** e clique no botão **`Re-run all jobs`** no canto superior direito.
3. Aguarde cerca de **1 minuto** até ficar com o ícone verde (✅) e atualize o site com **`Ctrl + F5`**:
   👉 **<https://minis-sesi.github.io/#/aulas>**

---

## 💡 Dicas importantes
- **Permissão da pasta:** Mantenha sempre a pasta do Google Drive com acesso **"Qualquer pessoa com o link pode visualizar"**, pois é assim que o robô do site consegue ler os PDFs e a planilha.
- **Apenas 1 PDF por pasta de aula:** Deixe dentro da pasta de cada aula apenas o PDF final que o professor deve baixar.
- **Tamanho do PDF:** Prefira PDFs de até ~25 MB para que o download seja rápido para os professores.
