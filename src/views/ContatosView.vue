<script setup>
import PageHeader from "../components/PageHeader.vue";
import { site as contato, redes } from "../data/conteudo";

const perguntas = [
  {
    p: "Preciso saber robótica para aplicar as aulas?",
    r: "Não. Cada aula traz a história, as atividades e o fechamento prontos. Basta ler o roteiro na página da aula antes de começar.",
  },
  {
    p: "Quanto custa usar o material?",
    r: "Nada. Os materiais são gratuitos para uso educacional. Pedimos apenas que os créditos às equipes sejam mantidos.",
  },
  {
    p: "Para qual idade são as aulas?",
    r: "As primeiras missões foram pensadas para crianças de 6 a 9 anos. A idade indicada aparece na página de cada aula.",
  },
  {
    p: "Minha escola ou ONG pode usar, mesmo não sendo do PEAL?",
    r: "Pode, sim! Adoraríamos saber onde o Mini S está sendo aplicado. Mande uma mensagem para a gente nas redes sociais.",
  },
];
</script>

<template>
  <div>
    <PageHeader
      eyebrow="Contatos"
      titulo="Fale com a gente"
      texto="Quer aplicar o Mini S, mandar fotos da sua turma ou dar uma sugestão? Chame as equipes nas redes sociais."
    />

    <section class="section">
      <div class="wrap">
        <div class="contact-grid">
          <a v-for="r in redes" :key="r.usuario" class="contact-card" :href="r.url" target="_blank" rel="noopener">
            <span class="contact-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5" /><circle cx="12" cy="12" r="4" /><circle cx="17.5" cy="6.5" r="1" fill="currentColor" /></svg>
            </span>
            <span class="contact-team">{{ r.equipe }}</span>
            <strong>@{{ r.usuario }}</strong>
            <span class="contact-go">Abrir no Instagram →</span>
          </a>

          <a v-if="contato.email" class="contact-card" :href="`mailto:${contato.email}`">
            <span class="contact-icon" aria-hidden="true">✉️</span>
            <span class="contact-team">E-mail</span>
            <strong>{{ contato.email }}</strong>
            <span class="contact-go">Enviar e-mail →</span>
          </a>
        </div>
        <p class="muted contact-place">📍 {{ contato.cidade }}</p>
      </div>
    </section>

    <section class="section tinted">
      <div class="wrap narrow">
        <span class="eyebrow">Dúvidas frequentes</span>
        <h2>Perguntas de professores</h2>
        <div class="faq">
          <details v-for="q in perguntas" :key="q.p">
            <summary>{{ q.p }}</summary>
            <p>{{ q.r }}</p>
          </details>
        </div>
      </div>
    </section>
  </div>
</template>
