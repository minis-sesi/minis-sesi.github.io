/*
 * Lê o conteúdo da pasta content/ (editado pelo painel /admin ou à mão).
 * Nada aqui precisa ser alterado para publicar uma aula nova.
 */
import siteJson from "../../content/site.json";
import galeriaJson from "../../content/galeria.json";

const arquivosAulas = import.meta.glob("../../content/aulas/*.json", { eager: true, import: "default" });
const arquivosEquipes = import.meta.glob("../../content/equipes/*.json", { eager: true, import: "default" });

// O painel salva arquivos como "/uploads/x.pdf". Sem a barra inicial o caminho
// funciona em qualquer endereço do GitHub Pages (usuario.github.io/repositorio/).
export function arquivo(caminho) {
  if (!caminho) return "";
  if (/^https?:\/\//.test(caminho)) return caminho;
  return caminho.replace(/^\/+/, "").replace(/^public\//, "");
}

// Aceita tanto o ID do vídeo quanto o link completo do YouTube.
export function youtubeId(valor) {
  if (!valor) return "";
  const m = String(valor).match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([\w-]{11})/);
  return m ? m[1] : String(valor).trim();
}

const lista = (v) => (Array.isArray(v) ? v.filter(Boolean) : []);

export const site = {
  totalEncontros: Number(siteJson.total_encontros) || 15,
  email: siteJson.email || "",
  cidade: siteJson.cidade || "",
  materialCompleto: arquivo(siteJson.material_completo),
  apoiadores: lista(siteJson.apoiadores).map((a) => ({ ...a, logo: arquivo(a.logo) })),
};

export const equipes = Object.values(arquivosEquipes)
  .map((e) => ({ ...e, logo: arquivo(e.logo) }))
  .sort((a, b) => (a.ordem ?? 99) - (b.ordem ?? 99));

export const galeria = lista(galeriaJson.fotos).map((f) => ({ ...f, imagem: arquivo(f.imagem) }));

const publicadas = Object.values(arquivosAulas)
  .filter((a) => a.numero && a.titulo && a.pdf && a.publicada !== false)
  .map((a) => {
    const paginas = lista(a.paginas).map(arquivo);
    return {
      ...a,
      id: Number(a.numero),
      status: "disponivel",
      pdf: arquivo(a.pdf),
      capa: arquivo(a.capa) || paginas[0] || "",
      paginas,
      video: youtubeId(a.video),
      habilidades: lista(a.habilidades),
      objetivos: lista(a.objetivos),
      roteiro: lista(a.roteiro),
      materiais: lista(a.materiais),
    };
  })
  .sort((a, b) => a.id - b.id);

export const aulasDisponiveis = publicadas;

// Trilha completa: aulas publicadas + vagas "em breve" até o total de encontros planejados.
const total = Math.max(site.totalEncontros, ...publicadas.map((a) => a.id), 0);
export const aulas = Array.from({ length: total }, (_, i) => {
  const id = i + 1;
  return publicadas.find((a) => a.id === id) || { id, status: "em-breve" };
});

export const series = [...new Set(publicadas.map((a) => a.serie).filter(Boolean))];
export const equipesComAula = [...new Set(publicadas.map((a) => a.equipe).filter(Boolean))];

export const redes = equipes
  .filter((e) => e.instagram)
  .map((e) => {
    const usuario = e.instagram.replace(/^@/, "").replace(/^https?:\/\/(www\.)?instagram\.com\//, "").replace(/\/.*$/, "");
    return { equipe: e.nome, usuario, url: `https://www.instagram.com/${usuario}/` };
  });
