<script>
  import Proposals from './Proposals.svelte';
  import Voters from './Voters.svelte';
  import Matrix from './Matrix.svelte';

  let proposals = [];
  let voters = [];

</script>

<main>
  <div class="row">
    <div class="column">
      <Proposals bind:proposals />
    </div>
    <div class="column">
      <Voters bind:voters />
    </div>
  </div>
  <Matrix bind:proposals bind:voters/>
</main>

<style>
	main {
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
  .row {
    display: flex;
  }

  .column {
    flex: 50%;
  }
</style>
