<script lang="ts">
	import Headers from '$lib/components/ui/headers.svelte';
	import "../global.css";
	import Footers from '$lib/components/ui/footers.svelte';

	let { children } = $props();
</script>
<head>
	<title>Dashboard</title>
</head>

<Headers />


<main>
	{@render children()}
</main>

<Footers />