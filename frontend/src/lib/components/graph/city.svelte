
<script lang="ts">
import { onMount } from 'svelte';
import { PieChart } from "layerchart";
import { Plot, BarX, setPlotDefaults } from 'svelteplot';
import {get_city} from '$lib/api/stats';



let { localisation_state, localisation_city, year } = $props();

setPlotDefaults({
    bar: {
        borderRadius: 4,
        stroke: 'currentColor',
        fill: "#dd4c4c"
    }
})

let city = $state<{
    customer__localisation__city:string;
    count:number;
}[]>([]);

$effect(async() => {
    city = await get_city(
            localisation_state,
            localisation_city,
            year
        );
});

</script>

<Plot
    y={{
        type: "band",
        label: "Villes",
        domain: city.map(c => c.customer__localisation__city)
    }}
    x={{
        type: "linear",
        label: "Nombre de commandes"
    }}
    >
    <BarX
        data={city}
        y="customer__localisation__city"
        x="count"
    />
</Plot>