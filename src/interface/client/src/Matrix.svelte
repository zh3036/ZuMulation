
<script>
  export let proposals = [];
  export let voters = [];
  export let matrix = [];

  function getMatrix(v, p) {
    if (v >= matrix.length || p >= matrix[0].length) {
      return NaN;
    }
    return matrix[v][p];
  }
</script>

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
            <td>{getMatrix(i, j)}</td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
</div>
