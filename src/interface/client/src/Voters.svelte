

<script>
  export let voters = [];

  function defaultData() {
    voters = [
      { enabled: true,
        name: 'Mary Green',
        preferences: "Persona: Environmental enthusiast, age 32, single, yoga instructor General Opinion on Zuzalu: Excited about the idea of living in an ecologically focused environment promoting a strong, healthy sense of community. Attitudes towards projects: Highly interested in health and wellness, renewable energy, and ecosystem conservations. Appreciates access to shared resources, creative culture, and sustainable transportation methods." },
      { enabled: true,
        name: 'Tom Sanders',
        preferences: " Persona: Entrepreneur, age 40, married, two kids, involved in the tech industry General Opinion on Zuzalu: Sees it as a smart way of living, intrigued by innovation and creative opportunities offered in such a space. Attitudes towards projects: Looks forward to collaborative workspaces, skill-sharing opportunities, and sustainable solutions in energy and food production. Appreciates health and wellness initiatives to achieve a better work-life balance." },
      { enabled: true,
        name: 'Rachel Thompson',
        preferences: " Persona: Artist, age 29, in a relationship, mural artist General Opinion on Zuzalu: Loves the idea of a creative and culturally thriving space with exciting opportunities for artists and creators. Attitudes towards projects: Enthusiastic about art and culture projects, community garden programs, and anything related to enhancing creativity. Appreciates the community-based actions leading to the environmental stewardship of multiple projects." },
      { enabled: true,
          name: 'Carlos Diaz',
        preferences: "Persona: Environmental engineer, age 37, married, interested in STEM subjects General Opinion on Zuzalu: Extensively fascinated by the potential to contribute expertise to develop more sustainable living spaces Attitudes towards projects: Highly keen on projects involving renewable energy infrastructure, waste management solutions, and technology-driven skill-sharing workshops. Wants to explore the world of art and culture for stress-relieving purposes." },
      { enabled: true,
        name: 'Angela Jenkins',
        preferences: " Persona: Single mom, age 35, raising two children alone, works from home as a marketing specialist General Opinion on Zuzalu: A potentially secure and supportive environment for her children to grow up and learn the importance of valuable community interaction. Attitudes towards projects: Primarily focused on the health and wellness program, the educational initatives, and the transportation & mobility promoting projects, as well as supportive and inclusive spaces like the resource library and the collaborative work zones." },
      { enabled: true,
        name: 'Louisa Hernandez',
        preferences: " Persona: Aspiring chef, age 25, just completed culinary education, co-living native since college General Opinion on Zuzalu: Planning to adopt an all-practical, cutting-edge model for healthy, sustainable lifestyles Attitudes towards projects: Extremely open to options that welcome her to innovate, actively participate, and contribute in new ways. Zones involving food production and transportation resonate, as well as the poised skill-sharing initiatives and health promotion activities at large." },
      { enabled: true,
        name: 'Samuel Wilson',
        preferences: " Persona: Architect, age 46, separated, devoted father and amateur cyclist General Opinion on Zuzalu: He’s hungry to join projects driving improvement in healthier urban landscape design, as it aligns with his worldview and principles. Attitudes towards this matter are expressed through his deep interest to contribute to solid renewable energy schemes, enhancing transportation, promoting ecosystem conservation-centric activities, and securing enough Rec and Tech facilities triggering creative development amongst dwellers in these spaces." }


    ];


  }
  defaultData();


</script>

<div>
  {#each voters as voter}
    <div class="voter">
      <label for="name">Voter name:</label>
      <input name="name" type="text" bind:value={voter.name} />
      <br/>
      <label for="preferences">Voter preferences:</label>
      <br/>
      <textarea name="preferences" rows=6 cols=50 bind:value={voter.preferences}></textarea>
      <br/>
      <label for="enabled">Enable this voter:</label>
      <input name="enabled" type="checkbox" bind:checked={voter.enabled} />
      <br/>
      <button type="button" on:click={() => voters = voters.filter(v => v !== voter)}>
        Remove voter
      </button>
    </div>
  {/each}
</div>
<br/>
<button type="button" on:click={() => voters = [...voters, { name: '', preferences: '', enabled: true}]}>
  Add voter
</button>
<style>
  .voter {
    border: 1px solid #ccc;
    padding: 1em;
    margin: 0.5em;
  }
  button {
    margin: 0.5em;
  }
</style>
