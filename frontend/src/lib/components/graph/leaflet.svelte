<script lang="ts">

import { onMount } from 'svelte';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import {initialize_map} from '$lib/api/stats';
import {get_map_data} from '$lib/api/stats';

let { localisation_state, localisation_city, year } = $props();

let locationLayer = $state<any>(null);
let map = $state<any>(null);
let L = $state<any>(null);

onMount(async () => {
    const result = await initialize_map();

    map = result.map;
    locationLayer = result.locationLayer;
    L = result.L;
});

$effect(() => {
    if (!locationLayer || !L) return;

    get_map_data(
        locationLayer,
        L,
        localisation_state,
        localisation_city,
        year
    );
});


</script>

<div id="map"></div>

<style>
    #map { 
        min-height: 25em;
    }
    @media (min-width:1440px){
        #map { 
            min-height: 50em;
        }
    }
</style>

