<script lang="ts">

    import { Plot, BarX, setPlotDefaults } from 'svelteplot';
    import { PieChart, Arc, Text } from "layerchart";
    import { onMount, onDestroy } from 'svelte';
    import Map_example from '$lib/Leaflet.svelte';

    //Variables

    let title_graph=$state("");

    let city = $state<{
        customer__localisation__city:string;
        count:number;
        }[]>([]);

    let showCityPlot = $state(false);

    let category = $state<{
        product_category_name:string;
        count:number;
    }[]>([]);


    let showCategoryPlot =$state(false);

    let payment = $state<{
        payment_type: string;
        count: number;
        percentage: string;
    }[]>([]);

    let showPaymentPlot =$state(false);

    let delivery = $state<{
        order_status: string;
        count: number;
        percentage: string;
    }[]>([]);

    let showDeliveryPlot =$state(false);

    let showAnyPlot = $derived(showCategoryPlot || showDeliveryPlot || showPaymentPlot);

    //Plots
    
    setPlotDefaults({
        bar: {
            borderRadius: 4,
            stroke: 'currentColor',
            fill: "#dd4c4c"
        }
    })

    //Functions

    async function get_city() {
        const response = await fetch('/api/stats_order_city');
        const data = await response.json();
        city = Object.values(data);
        showCityPlot = true;
    }

    async function get_category() {
        const response = await fetch('/api/stats_categories');
        const data = await response.json();
        category = data.map(item => ({
            ...item,
            product_category_name:item.product_category_name
                .replace(/_/g, ' ')
                .toLowerCase()
                .replace(/^./, char => char.toUpperCase())
        }))
        title_graph="Catégories";
        showCategoryPlot = true;
        showPaymentPlot = false;
        showDeliveryPlot = false;
    }

    async function get_payment() {
        const response = await fetch('/api/stats_payment_type');
        const data = await response.json();
        payment = data.map(item => ({
            ...item,
            payment_type :item.payment_type
                .replace(/_/g, ' ')
                .toLowerCase()
                .replace(/^./, char => char.toUpperCase())
        }))

        // Supprimer les catégories qui représentent moins de 2 %
        const total = payment.reduce((sum, item) => sum + item.count, 0);

        payment = payment
            .filter(item => item.count / total >= 0.002)
            .map(item => ({
                ...item,
                percentage: ((item.count / total) * 100).toFixed(1)
        }));

        title_graph="Paiements";
        showPaymentPlot = true;
        showCategoryPlot = false;
        showDeliveryPlot = false;
    }

    async function get_delivery(){
        const response = await fetch('/api/stats_orders');
        const data = await response.json();
        const total = data.reduce(
            (sum, item) => sum + item.count,
            0
        );
        delivery= data.map(item =>({
            ...item,
            order_status:item.order_status
                .replace(/_/g, ' ')
                .toLowerCase()
                .replace(/^./, char => char.toUpperCase())
        }))
        delivery = delivery
                    .filter(item => item.count / total >= 0.002)
                    .map(item => ({
                        ...item,
                        percentage: ((item.count / total) * 100).toFixed(1)
                }));
        title_graph="Livraisons";
        showPaymentPlot = false;
        showCategoryPlot = false;
        showDeliveryPlot = true;
    }


</script>

<div class="content">
    <div class=title_page>
        <h1>Dashboard</h1>
    </div>
    <p>Suivez l’évolution de vos commandes et de vos livraisons ainsi que des catégories les plus populaires et plus encore.</p>

    <br>
    <div class="graph_title">
        <h1 style:display={title_graph ? "block" :"none"}>{title_graph}</h1>
    </div>
    <div class="graph" class:active={showAnyPlot}>
        {#if showCategoryPlot}
            <Plot
                y={{
                    type: "band",
                    label: "Category",
                    domain: category.map(c => c.product_category_name)
                }}
                x={{
                    type: "linear",
                    label: "Nombre de commandes"
                }}
            >
                <BarX
                    data={category}
                    y="product_category_name"
                    x="count"
                />
            </Plot>
        {/if}
        {#if showDeliveryPlot}
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
        {/if}
        {#if showPaymentPlot}
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
        {/if}
    </div>
    <div class ="background-filters">
        <div class="filters">
            <button onclick={get_category}>Catégories</button>
            <button onclick={get_delivery}>Livraisons</button>
            <button onclick={get_payment}>Paiement</button>
        </div>
    </div>
    <br><br>
    
    <div class="graph">
        {#if showCityPlot}
            <Plot
                y={{
                    type: "band",
                    label: "Ville",
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
        {/if}
    </div>
    <div class ="background-filters">
        <div class="filters">
            <button onclick={get_city}>Villes populaires</button>
        </div>
    </div>
    <Map_example/>
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
        background: rgba(0, 0, 0, 0.05);
        display:flex;
        justify-content:space-around;
        border-radius: 5% / 90%;
    }
    .filters button{
        background: rgba(233, 124, 124, 0.0);
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
    }

    @media (min-width:1440px){
        .content{
            padding:1rem 4rem;
        }
        .graph_title h1{
            padding: 0px 25% 0px 25%;
        }
        .graph{
            padding: 0px 25% 0px 25%;
            display:flex;
            align-items:center;
            justify-content:center;
        }
        .graph.active{
            height:50vh;
        }
        .graph img{
            width:0%;
        }
        
        .filters{
            padding:0.5% 0.5%;
            width:40%;
        }

        .background-filters{
            display:flex;
            justify-content:center;
        }
    }
</style>