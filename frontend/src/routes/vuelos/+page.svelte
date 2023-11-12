<script>
    // @ts-nocheck
    import { onDestroy, onMount } from 'svelte';
    import { PUBLIC_BASE_URL } from '$env/static/public'
	import { SyncLoader } from 'svelte-loading-spinners';
    import Navbar from '../../components/Navbar.svelte';
	import { createSearchStore, searchHandler } from '$lib/stores/search';
     
    let searchedFlights = []
    let searchStore = null;
    let unsubscribe = null;

    let page = 0;
    let pagination = 15;

    let current_sort_key = "";
    let sort_dir = 1;

    let loading = true;

    function sort_by(attribute) {
        if (attribute === current_sort_key) {
            sort_dir *= -1;
        } else {
            sort_dir = 1;
        }

        $searchStore.data = $searchStore.data.sort((a, b) => (a[attribute] > b[attribute]) ? sort_dir : -sort_dir);

        current_sort_key = attribute;
    }

    function change_page(dir) {
        if (0 <= page + dir && page + dir < $searchStore.data.length / pagination) {
            page += dir
        }
        document.body.scrollIntoView();
    }

    function change_to_page(p) {
        page = p
        document.body.scrollIntoView();
    }

    onMount(async () => {
        loading = true;

        const response = await fetch(PUBLIC_BASE_URL+"/vuelos");
        const vuelos = await response.json();
        searchedFlights = vuelos.map( vuelo => ({
            ...vuelo,
            searchTerms: `${vuelo.city_x} ${vuelo.destination} ${vuelo.city_y} ${vuelo.origin}`
        }))
        searchStore = createSearchStore(searchedFlights);
        unsubscribe = searchStore.subscribe(model => searchHandler(model))

        loading = false;
    });

    onDestroy(() => {
        if (unsubscribe !== null) {
            unsubscribe();
        }
    })

</script>

<Navbar />

<h1>Flights</h1>

<div id="table">
    {#if loading}
        <div class="spinner">
            <SyncLoader color="#F8F8F8"/>
        </div>
    {:else}

    <input type="search" placeholder="Search city" bind:value={$searchStore.search}>

    <table>
        <tr id="table-titles">
            <th>Flight Number <button on:click={()=>sort_by('flightNumber')}>s</button></th>
            <th>Origin <button on:click={()=>sort_by('origin')}>s</button></th>
            <th>Destination <button on:click={()=>sort_by('destination')}>s</button></th>
            <th>Airline <button on:click={()=>sort_by('airline')}>s</th>
            <th>Avg Age <button on:click={()=>sort_by('averageAge')}>s</th>
            <th>Total Distance <button on:click={()=>sort_by('dist_recorrida')}>s</th>
            <th>Plane <button on:click={()=>sort_by('aircraftName')}>s</th>
            <th>#Passengers <button on:click={()=>sort_by('passengersQty')}>s</th>
        </tr>

        {#each $searchStore.filtered.slice(page*pagination, (page+1)*pagination) as vuelo}
        <tr class="table-item" on:click={()=>console.log(vuelo)}>
            <td>
                <a href={`/map/${vuelo.flightNumber}`}>{vuelo.flightNumber}</a>
            </td>
            <td>{vuelo.city_x}, {vuelo.origin}</td>
            <td>{vuelo.city_y}, {vuelo.destination}</td>
            <td>{vuelo.airline}</td>
            <td>{vuelo.averageAge.toFixed(2)} years</td>
            <td>{vuelo.distance.toFixed(2)} km</td>
            <td>{vuelo.aircraftName}</td>
            <td>{vuelo.passengersQty}</td>
        </tr>
        {/each}
    </table>
    <div id="page">
        <button on:click={()=>change_page(-1)}>left</button>
        {#each Array.from({length: 10}, (_, i) => i + page - 5).filter(v=> v >= 0) as page_number}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            {#if page_number===page}
                <div on:click={()=>change_to_page(page_number)} class="current-page page-number">{page_number+1}</div>
            {:else}
                <div on:click={()=>change_to_page(page_number)} class="page-number">{page_number+1}</div>
            {/if}
        {/each}
        <button on:click={()=>change_page(1)}>right</button>
    </div>
    {/if}
</div>

<style>
    h1 {
        font-size: 50pt;
        text-align: center;
        margin: 0rem 0rem 1rem 0rem;
    }

    .spinner {
        width: 1000px;
    }

    #table {
        display: flex;
        flex-direction: column;
        justify-content: center;
        background-color: #303138; 
        border-radius: 15px;
        max-width:fit-content;
        margin: 1rem;
    }

    table {
        margin: 1rem 1rem;

        font-family: arial, sans-serif;
        border-collapse: collapse;

        display: block;
        overflow-x: auto;
        table-layout: fixed; 
    }
    
    th, td {
        text-align: left;
        padding: 18px;

    }

    th {
        border-bottom: 1px solid #8689A2;
        color: #8689A2;
        
        /* width: 1000px; */
        white-space: nowrap;
        /* max-width: 100px;
        overflow: hidden;
        white-space: nowrap; */
    }

    td {
        border-top: 1px solid #8689A2;
        
        /* width: 1000px; */
        max-width: 1000px;
        overflow: hidden;
        /* white-space: nowrap; */
    }

    /* #table-titles :nth-child(0) { */
        /* width: 4rem; */
        /* overflow-wrap: break-word; */
        /* overflow: hidden; */
        /* background-color: rgba(150, 212, 212, 0.4); */
    /* } */

    #page {
        display: flex;
        justify-content: center;

        height: 2rem;
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        background-color: red;
    }

    .page-number {
        margin-right: 6px;
    }

    .current-page {
        font-weight: bolder;
    }
</style>