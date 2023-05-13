
<script>
  export let proposals = [];
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
