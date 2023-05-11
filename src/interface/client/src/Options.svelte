
<script>
  export let options = [];
</script>

<div>
  {#each options as option}
    <div>
      <label for="name">Option name:</label>
      <input name="name" type="text" bind:value={option.name} />
      <br/>
      <label for="enabled">Enable this option:</label>
      <input name="enabled" type="checkbox" bind:checked={option.enabled} />
      <br/>
      <label for="description">Option description:</label>
      <br/>
      <textarea name="description" rows=6 cols=50 bind:value={option.description}></textarea>
    </div>
  {/each}
</div>
<button type="button" on:click={() => options = [...options, { name: '', enabled: true, description: '' }]}>
  Add option
</button>
