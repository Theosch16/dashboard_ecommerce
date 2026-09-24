<script lang="ts">
    import { onMount } from 'svelte';
    import Map from '$lib/components/graph/leaflet.svelte';
    import Payment from '$lib/components/graph/payment.svelte';
    import City from '$lib/components/graph/city.svelte';
    import Delivery from '$lib/components/graph/delivery.svelte';
    import Category from '$lib/components/graph/category.svelte';

    import Filters from '$lib/components/filters/search.svelte';

	let selected = $state({
        localisation_state: '',
        localisation_city: '',
        year: ''
    });

    function updateFilters(state,city,year){
        selected = {
            localisation_state:state,
            localisation_city:city,
            year:year
        };
    }

</script>

<div class="content">
    <div class=title_page>
        <h1>Dashboard</h1>
    </div>
    <p>Suivez l’évolution de vos commandes et de vos livraisons ainsi que des catégories les plus populaires et plus encore.</p>

    <br>
    <div class ="background-filters">
        <div class="filters">
            <Filters onConfirm={updateFilters} />
        </div>
    </div>

    <div class="dashboard_grid">
        <div class="grid_content">
            <h1>Catégories les plus populaires</h1>
            <div class="graph">
                <Category
                    localisation_state={selected.localisation_state}
                    localisation_city={selected.localisation_city}
                    year={selected.year}
                />
            </div>
        </div>

        <div class="grid_content">
            <h1>Statut des livraisons</h1>
            <div class="graph">
                <Delivery
                    localisation_state={selected.localisation_state}
                    localisation_city={selected.localisation_city}
                    year={selected.year}
                />
            </div>
        </div>
        
        <div class="grid_content">
            <h1>Type de paiements</h1>
            <div class="graph">
                <Payment
                    localisation_state={selected.localisation_state}
                    localisation_city={selected.localisation_city}
                    year={selected.year}
                />
            </div>
        </div>

        <div class="grid_content">
            <h1>Villes les plus populaires</h1>
            <div class="graph">
                <City
                    localisation_state={selected.localisation_state}
                    localisation_city={selected.localisation_city}
                    year={selected.year}
                />
            </div>
        </div>
        <div class="grid_content">
            <h1>Carte des commandes</h1>
            <div class="map_container">
                <Map
                    localisation_state={selected.localisation_state}
                    localisation_city={selected.localisation_city}
                    year={selected.year}
                />
            </div>
        </div>
    </div>
</div>

<style>

    :global(.payment-legend) {
        width:100%;
        display:grid;
        justify-content:center;
        padding-bottom:10px;
    }
    :global(.payment-legend *) {
        display:grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
    }
    :global(.payment-legend button) {
        display:flex;
        align-items:center;
        justify-content:flex-start;
        border:0;
        background-color: rgb(255 255 255 / 0);
        font-family:Inter;
        font-size:1em;
    }

    .graph :global(svg) {
        max-width: 100%;
        height: auto;
        display: block;
    }

    .title_page h1{
        font-weight: 500;
        font-size:2.5rem;
        letter-spacing:-0.02em;
    }

    .content{
        padding:2rem;
    }
    Plot{
        display:flex;
        justify-content:center;
    }
    .content p{
        letter-spacing:-0.002em;
        font-weight: 400;
        opacity:0.45;
        text-align:justify;
    }
    .filters {
        display:grid;
        gap:2%;
        grid-template-columns: 1fr 1fr 1fr 0.5fr;
    }
    .filters button{
        background: rgba(134, 36, 36, 0);
        border-color:transparent;
        font-weight: 400;
        font-family : Inter;
    }
    
    @media (max-width:800px){
        :global(.payment-legend *) {
            display:grid;
            justify-content:space-around;
            grid-template-columns: 1fr 1fr;
            
        }
        .filters {
            display:grid;
            grid-template-columns: 1fr 1fr;
        }
    }

    @media (min-width:1440px){

        .content{
            padding:1rem 4rem;
        }
        .grid_content h1{
            padding: 0px 10% 0px 10%;
        }
        .graph{
            padding: 0px 10% 0px 10%;
            align-items:center;
            justify-content:center;
        }
        .graph.active{
            height:50vh;
        }
        
        .filters{
            padding:0.5% 0.5%;
            width:40%;
        }

        .background-filters{
            display:flex;
            justify-content:center;
        }
        .dashboard_grid{
            padding-top:1rem;
            display:grid;
            grid-template-columns:1fr 1fr;
        }
        .grid_content{
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.06);
        }
        .map_container{
            padding: 0px 10% 2% 10%;
        }
        .dashboard_grid > .grid_content:last-child {
            grid-column: 1 / -1;
        }
    }
</style>