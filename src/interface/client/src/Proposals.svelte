
<script>
  export let proposals = [];


  function defaultData() {
    proposals = [
      { enabled: true,
        name: 'Sustainable Food Production System',
        description: 'As an aspiring chef with a culinary education, I am passionate about turning locally-grown and sustainably sourced ingredients into delicious culinary creations. I believe this project could provide valuable resources and inspire community residents, including myself, in innovative and sustainable cooking practices while also reducing our carbon footprint.',
        outcome: 'The community produces food more sustainably, reducing carbon footprinte.'},
      { enabled: true,
        name: 'Skill-Sharing and Educational Initiatives',
        description: "We can never stop learning, improving and sharing our knowledge with others. Combining culinary education and experience with others' skill sets will only lead to a more vibrant and multifaceted community. I look forward to expanding my own horizons as well as having the opportunity to teach cooking classes and share my passion for food with my fellow community members.",
        outcome: 'More people in the community learn how to cook.'},
      { enabled: true,
          name: 'Transportation and Mobility Promoting',
          description: "Being an advocate for healthy living and sustainability, ensuring efficient and environment-friendly mobility options is important. Commuting to local farmers' markets and other food sourcing without negatively impacting the environment is both practical and appealing for me. Investing in bike-shares and community-friendly pathways will also encourage a more active lifestyle and foster community-wide connections.",
          outcome: 'More people in the community are riding bikes, they exercise more and pollute less.'},
      { enabled: true,
        name: 'a cigarette and alchohol shop',
        description: " sell cigarretees, can generate profit for the community.",
        outcome: 'More people in the community buy cigarettes and alcohol, there are some health problems, but the shop generates profit that gets taxed.'},
      { enabled: true,
        name: 'Art and Culture Enrichment',
        description: "A healthy dose of art and culture can breathe life into any community. As an appreciator of art, I believe dedicated gallery spaces, workshops, and other creative projects will not only foster our home-grown artistic expressions but also incorporate creativity into our everyday lives, potentially blending with food production and healthy living.",
        outcome: 'There are more art galleries featuring art by community members, it is more common to see artwork when walking around the community.'},
    ];
  }
  defaultData();



</script>

<div>
  {#each proposals as proposal}
    <div class="proposal">
      <label for="name">Proposal name:</label>
      <input name="name" type="text" bind:value={proposal.name} />
      <br/>
      <label for="enabled">Enable this proposal:</label>
      <input name="enabled" type="checkbox" bind:checked={proposal.enabled} />
      <br/>
      <label for="description">Proposal description:</label>
      <br/>
      <textarea name="description" rows=6 cols=50 bind:value={proposal.description}></textarea>
      <br/>
      <label for="outcome">Proposal outcome:</label>
      <br/>
      <textarea name="outcome" rows=6 cols=50 bind:value={proposal.outcome}></textarea>
      <br/>
      <button type="button" on:click={() => proposals = proposals.filter(o => o !== proposal)}>
        Remove proposal
      </button>
    </div>
  {/each}
</div>
<br/>
<button type="button" on:click={() => proposals = [...proposals, { name: '', enabled: true, description: '', outcome: '' }]}>
  Add proposal
</button>

<style>
  .proposal {
    border: 1px solid #ccc;
    padding: 1em;
    margin: 0.5em;
  }
  button {
    margin: 0.5em;
  }
</style>
