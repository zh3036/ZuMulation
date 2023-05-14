
<script>

  import SvelteTooltip from 'svelte-tooltip';

  export let proposals = [];
  export let voters = [];
  export let matrix = [];
  export let proposalDicts = [];
  export let voterDicts = [];

  async function refreshMatrix() {
    let response = await fetch("/api/getmatrix", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        voters: voters,
        proposals: proposals,
      }),
    });
    let json = await response.json();
    console.log('json', json);
    matrix = json[0].preferenceMatrix;
    voterDicts = json[1];
    proposalDicts = json[2];
  }
</script>

<button type="button" on:click={refreshMatrix}>
  Refresh utility matrix
</button>
<div>
  <table>
    <thead>
      <tr>
        <th></th>
        {#each proposals as proposal, i}
          <th><SvelteTooltip tip={i >= proposalDicts.length ? "" : JSON.stringify(proposalDicts[i])} color="#CCCCCC">{proposal.name}</SvelteTooltip></th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each voters as voter, i}
        <tr>
          <th><SvelteTooltip tip={i >= voterDicts.length ? "" : JSON.stringify(voterDicts[i])} color="#CCCCCC">{voter.name}</SvelteTooltip></th>
          {#each proposals as proposal, j}
            {#if (i >= matrix.length || j >= matrix[0].length)}
              <td>N/A</td>
            {:else}
              <td>{matrix[i][j]}</td>
            {/if}
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
</div>
