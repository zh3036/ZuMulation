
<script>
  export let proposals = [];


  function defaultData() {
    proposals = [
      { enabled: true,
        name: 'Zuzalu Stay Connected',
        description: 'A community connection and planning coordination app. The app collects data overtime to help residents make informed decisions about their lifestyle and community involvement. It also provides a platform for residents to share their ideas and collaborate on projects.',
        outcome: ''},
      { enabled: true,
        name: 'ZK Community Currency',
        description: "A private currency for Zuzalu. We want to use this currency to aid inequality by providing private air drops to those who are still building their wealth. We want this to be private because we do not want to expose sensitive details.",
        outcome: ''},
      { enabled: true,
          name: 'Weekly Biomarker Tracking',
          description: "We will pay for biomarker tracking for all residents. This will help us understand the health of our community and help us make informed decisions about our lifestyle and community involvement.",
          outcome: ''},
      { enabled: true,
        name: 'Skill-Sharing and Educational Initiatives Days',
        description: "Enabling knowledge to be efficiently shared and acquired through skill-based workshops, mentoring programs, and a community-run learning center, this project focuses on developing the collective skills of community members.",
        outcome: ''},
      { enabled: true,
        name: 'Communal Resource Hub',
        description: "A shared resource hub on GitHub will facilitate knowledge-sharing and saving among the community members. This hub will consist of books, papers, equipment, and more, promoting a lending rather than owning mentality.",
        outcome: ''},
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
