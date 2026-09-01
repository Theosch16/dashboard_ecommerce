<script>
    import {page} from '$app/state';
</script>

<header class="header">
    {#if page.url.pathname === '/'}
		<h1>Accueil</h1>
    {:else if page.url.pathname === '/about'}
		<h1>A propos</h1>
    {:else}
		<h1>Dashboard</h1>
	{/if}
    <div class="navheader">
        <p><a href="http://localhost:5173">Accueil</p>
        <p><a href="http://localhost:5173/dashboard">Dashboard</p>
        <p><a href="http://localhost:5173/about">A propos</a></p>
    </div>
</header>

<style>

    .header{
        background-color:var(--color-background);
        color:var(--color-white);
        padding-left:2rem;
        padding-right:2rem;
        padding-bottom:0.5rem;
        padding-top:1rem;
    }

    .header a{
    text-decoration:none;
    color:inherit;
    }

    .header h1{
        font-weight: 900;
        font-size:3rem;
        margin:0;
        letter-spacing:-0.02em;
    }

    .navheader{
        display:flex;
        gap: 1.5rem;
        justify-content:left;
    }
    .navheader p{
        font-size: 1.2rem;
        font-weight: 400;
        letter-spacing:-0.005em;
    }
    @media(min-width: 1440px) {
        .header{
            padding-left:4rem;
            padding-right:4rem;
            padding-bottom:1rem;
            padding-top:2rem;
        }
    }
</style>
