import { ref } from "vue";

const LIMITE_PAGINAS = 24;

/*
 * Gera imagens das páginas de um PDF no navegador (pdf.js).
 * Usado quando a aula foi publicada só com o PDF, sem imagens das páginas.
 * O pdf.js só é baixado quando essa função roda.
 */
export function usePdfPaginas() {
  const paginas = ref([]);
  const carregando = ref(false);
  const erro = ref(false);

  async function gerar(url) {
    carregando.value = true;
    erro.value = false;
    paginas.value = [];
    try {
      const pdfjs = await import("pdfjs-dist");
      const worker = await import("pdfjs-dist/build/pdf.worker.min.mjs?url");
      pdfjs.GlobalWorkerOptions.workerSrc = worker.default;

      const doc = await pdfjs.getDocument({ url: new URL(url, location.href).href }).promise;
      const total = Math.min(doc.numPages, LIMITE_PAGINAS);
      for (let n = 1; n <= total; n++) {
        const pagina = await doc.getPage(n);
        const base = pagina.getViewport({ scale: 1 });
        const viewport = pagina.getViewport({ scale: 1100 / base.width });
        const canvas = document.createElement("canvas");
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        await pagina.render({ canvasContext: canvas.getContext("2d"), viewport }).promise;
        const blob = await new Promise((ok) => canvas.toBlob(ok, "image/jpeg", 0.82));
        paginas.value = [...paginas.value, URL.createObjectURL(blob)];
      }
    } catch (e) {
      console.error("Não foi possível gerar a prévia do PDF", e);
      erro.value = true;
    } finally {
      carregando.value = false;
    }
  }

  function limpar() {
    paginas.value.forEach((u) => URL.revokeObjectURL(u));
    paginas.value = [];
  }

  return { paginas, carregando, erro, gerar, limpar };
}
