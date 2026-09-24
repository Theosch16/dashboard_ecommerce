
<script lang="ts">
import { onMount } from 'svelte';
import { PieChart } from "layerchart";
import {get_payment} from '$lib/api/stats';

let { localisation_state, localisation_city, year } = $props();

let payment = $state<{
    payment_type: string;
    count: number;
    percentage: string;
}[]>([]);



$effect(async() => {
    payment = await get_payment(
            localisation_state,
            localisation_city,
            year
        );
});

</script>

<PieChart
    data={payment}
    key="payment_type"
    value="count"
    label={(d) => `${d.payment_type} (${d.percentage}%)`}
    padding={{ top: 24, bottom: 65 }}
    legend={{
        classes: {
            root: "payment-legend",
            swatch: "payment-swatch",
            label: "payment-label"
        }
    }}
    height={400}
/>