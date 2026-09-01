<script lang="ts">
	import Headers from '$lib/components/ui/headers.svelte';
	import "../global.css";
	import Footers from '$lib/components/ui/footers.svelte';

	let { children } = $props();
</script>
<head>
	<title>Dashboard</title>
</head>
<div class="container">
	<Headers />


	<main>
		{@render children()}
	</main>

	<Footers />
</div>

<style>

	.container{
		display:grid;
		grid-template-rows: auto 1fr auto;
		min-height:100vh;
	}

</style>