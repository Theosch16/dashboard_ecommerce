<script lang="ts">

import { onMount } from 'svelte';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'


//Wait for the navigator to start
onMount(async () =>{

    const leaflet = await import('leaflet');
    const L = leaflet.default ?? leaflet;
    (window as any).L = L;
    await import('leaflet.markercluster');

    var map = L.map('map').setView([-23.547, -46.640], 4);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    try {
        const response= await fetch("api/stats_order_locations/");
        if (!response.ok){
            throw new Error(`Response status:${response.status}`);
        }
        const result=await response.json();
        console.log(result);
        result.forEach((result)=>{
            const circle = L.circle([
                result.latitude,
                result.longitude,
            ],
            {
                radius: 2500,
            }
            ).addTo(map);

            circle.bindPopup(`
                <strong>Ville :</strong> ${result.city}<br>
                <strong>Commandes :</strong> ${result.count}

            `);
        });
    }
    catch(error){
        console.error(error.message);
    }

})





</script>

<div id="map"></div>

<style>
    #map { 
        min-height: 25em;
    }
</style>

