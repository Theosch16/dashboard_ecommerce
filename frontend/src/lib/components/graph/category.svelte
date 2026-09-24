
<script lang="ts">
import { onMount } from 'svelte';
import { PieChart } from "layerchart";
import { Plot, BarX, setPlotDefaults } from 'svelteplot';
import {get_category} from '$lib/api/stats';


setPlotDefaults({
    bar: {
        borderRadius: 4,
        stroke: 'currentColor',
        fill: "#dd4c4c"
    }
})

let { localisation_state, localisation_city, year } = $props();

let category = $state<{
    product_category_name:string;
    count:number;
}[]>([]);


$effect(async() => {
    category = await get_category(
        localisation_state,
        localisation_city,
        year
    );
});


</script>



<Plot
    y={{
        type: "band",
        label: "Catégories",
        domain: category.map(c => c.product_category_name)
    }}
    x={{
        type: "linear",
        label: "Nombre d'articles commandés"
    }}
>
    <BarX
        data={category}
        y="product_category_name"
        x="count"
    />
</Plot>