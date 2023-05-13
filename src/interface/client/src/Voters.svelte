

<script>
  export let voters = [];
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
