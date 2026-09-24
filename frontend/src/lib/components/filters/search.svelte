
<script lang="ts">
    import { onMount } from 'svelte';
    import {get_category} from '$lib/api/stats';

    let states=$state<string[]>([]);
    let cities=$state<string[]>([]);
    let years= $state<number[]>([]);
    
    let selected_State= $state('');
    let selected_Cities= $state('');
    let selected_Years= $state('');

    let { onConfirm } = $props();

    async function get_data() {
        const url=selected_State
            ? `/api/filters?state=${selected_State}`
            : '/api/filters';

        const response = await fetch(url);
        const data = await response.json();

        states=data.states;
        cities=data.cities;
        years=data.years;
    }
    
    async function confirmFilters() {
        onConfirm(
            selected_State,
            selected_Cities,
            selected_Years
        )
    }

    $effect(() => {
        if (selected_State){
            selected_Cities = '';
            get_data();
        }
    });

    onMount(() => {
            get_data();
    });

</script> 

<select bind:value={selected_State}>
    <option value="">Tous les États</option>

    {#each states as state}
        <option value={state}>
            {state}
        </option>
    {/each}
</select>

<select bind:value={selected_Cities}>
    <option value="">Toutes les villes</option>

    {#each cities as city}
        <option value={city}>
            {city}
        </option>
    {/each}
</select>

<select bind:value={selected_Years}>
    <option value="">Toutes les années</option>
    {#each years as year}
        <option value={year}>
            {year}
        </option>
    {/each}
</select>

<button onclick={confirmFilters}>
    Confirmer
</button>

<style>

    select{
        background: rgba(0, 0, 0, 0.05);
        border:1px solid black;
        padding:5%;
        border-radius:20px;
        width:100%;
    }
    
    select:hover{
        cursor:pointer;
    }

    button{
        border:1px solid black;
        border-radius:20px;
    }

    button:hover{
        cursor:pointer;
    }

    @media (max-width:800px){
        select{
            margin-bottom:10%;
        }
        button{
            margin-bottom:10%;
        }
    }


</style>