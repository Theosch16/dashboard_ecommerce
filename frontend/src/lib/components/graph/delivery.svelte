
<script lang="ts">
import { onMount } from 'svelte';
import { PieChart } from "layerchart";
import {get_delivery} from '$lib/api/stats';


let { localisation_state, localisation_city, year } = $props();


let delivery = $state<{
        order_status: string;
        count: number;
        percentage: string;
    }[]>([]);


$effect(async() => {
    delivery = await get_delivery(
        localisation_state,
        localisation_city,
        year
    );
});

</script>

<PieChart
    data={delivery}
    key="order_status"
    value="count"
    innerRadius={-40}
    padding={{ top: 24, bottom: 85}}
    label={(d) => `${d.order_status} (${d.percentage}%)`}
    legend={{
        classes: {
            root: "payment-legend",
            swatch: "payment-swatch",
            label: "payment-label"
        }
    }}
    height={400}
/>