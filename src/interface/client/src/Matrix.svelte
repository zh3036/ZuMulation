
<script>
  export let proposals = [];
  export let voters = [];
  export let matrix = [];

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
    matrix = json.preferenceMatrix;
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
        {#each proposals as proposal}
          <th>{proposal.name}</th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each voters as voter, i}
        <tr>
          <th>{voter.name}</th>
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
