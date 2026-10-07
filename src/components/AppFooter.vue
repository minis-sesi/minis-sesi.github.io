<script setup>
import { redes } from "../data/conteudo";
const ano = new Date().getFullYear();
</script>

<template>
  <footer class="footer">
    <div class="wrap footer-grid">
      <div>
        <img class="footer-logo" src="img/logo-srobots.png" alt="S Robots" />
        <p>Mini S: um projeto educacional e social das equipes de robótica da Escola SESI de Jaraguá do Sul.</p>
      </div>
      <div>
        <h3>Navegue</h3>
        <ul>
          <li><RouterLink to="/quem-somos">Quem somos</RouterLink></li>
          <li><RouterLink to="/sobre">Sobre o projeto</RouterLink></li>
          <li><RouterLink to="/aulas">Aulas</RouterLink></li>
          <li><RouterLink to="/contatos">Contatos</RouterLink></li>
          <li><a href="admin/" rel="nofollow">🔒 Área da equipe</a></li>
        </ul>
      </div>
      <div>
        <h3>Siga as equipes</h3>
        <ul>
          <li v-for="r in redes" :key="r.usuario">
            <a :href="r.url" target="_blank" rel="noopener">@{{ r.usuario }}</a>
          </li>
        </ul>
      </div>
      <p class="copy">
        © {{ ano }} Mini S · S ROBOTS e S ATLAS · Escola SESI Jaraguá do Sul. Materiais de uso livre para fins educacionais.
      </p>
    </div>
  </footer>
</template>
