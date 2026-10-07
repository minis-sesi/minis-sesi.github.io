import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// base "./" faz o site funcionar em qualquer endereço do GitHub Pages
// (usuario.github.io/nome-do-repo) sem precisar configurar o nome do repositório.
export default defineConfig({
  // Imagens e PDFs ficam em public/ e são referenciados como "img/..." e "pdf/...",
  // então o Vue não deve tentar importá-los como módulos.
  plugins: [vue({ template: { transformAssetUrls: false } })],
  base: "./",
});
