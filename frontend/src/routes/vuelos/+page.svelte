<script>
    // @ts-nocheck
    import { onDestroy, onMount } from 'svelte';
    import { PUBLIC_BASE_URL } from '$env/static/public'
	import { SyncLoader } from 'svelte-loading-spinners';
    import Navbar from '../../components/Navbar.svelte';
	import { createSearchStore, searchHandler } from '$lib/stores/search';
	import SortingIcon from '../../components/SortingIcon.svelte';
     
    let searchedFlights = []
    let searchStore = null;
    let unsubscribe = null;

    let page = 0;
    let pagination = 15;

    let current_sort_key = "";
    let sort_dir = 1;
    let titles = [ // state = "both", "up", "down"
        {name: "Flight Number", key:"flightNumber", state:"all"} ,
        {name: "Origin", key:"origin", state:"all"} ,
        {name: "Destination", key:"destination", state:"all"} ,
        {name: "Airline", key:"airline", state:"all"} ,
        {name: "Avg Age", key:"averageAge", state:"all"} ,
        {name: "Total Distance", key:"distance", state:"all"} ,
        {name: "Plane", key:"aircraftName", state:"all"} ,
        {name: "No. Passengers", key:"passengersQty", state:"all"},
    ]

    let loading = true;

    function sort_by(attribute) {
        for (let i = 0; i < titles.length; i++) {
            if (titles[i].key==attribute) {
                if (attribute === current_sort_key) {
                    if (sort_dir < 0) {
                        titles[i].state = "down"
                    } else {
                        titles[i].state = "up"
                    }
                    sort_dir *= -1;
                } else {
                    sort_dir = 1;
                    titles[i].state = "down"
                }
            } else {
                titles[i].state = "all"
            }
        }

        $searchStore.data = $searchStore.data.sort((a, b) => (a["flightNumber"] > b["flightNumber"]) ? sort_dir : -sort_dir);
        $searchStore.data = $searchStore.data.sort((a, b) => (a["month"] > b["month"]) ? sort_dir : -sort_dir);
        $searchStore.data = $searchStore.data.sort((a, b) => (a["year"] > b["year"]) ? sort_dir : -sort_dir);
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
        sort_by("year")

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

<div id="table-container">
    <div id="table">
        {#if loading}
            <div class="spinner">
                <SyncLoader color="#F8F8F8"/>
            </div>
        {:else}
            <input type="search" placeholder="Search city" bind:value={$searchStore.search}>
            <table>
                <tr id="table-titles">
                    {#each titles as data}
                        <th>
                            <div id="table-header">
                                <div id="table-title">{data.name}</div>
                                <SortingIcon 
                                    onClickFunction={()=>sort_by(data.key)}
                                    bind:data={data}
                                /> 
                            </div>
                        </th>
                    {/each}
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
</div>

<style>
    h1 {
        font-size: 50pt;
        text-align: center;
        margin: 0rem 0rem 1rem 0rem;
    }

    .spinner {
        width: 100%;
        display: flex;
        justify-content: center;
    }

    #table-container {
        display: flex;
        justify-content: center;
        padding: 2rem
    }

    #table {
        display: flex;
        flex-direction: column;
        justify-content: center;
        background-color: #303138; 
        box-shadow: 0px 0px 25px #151518;
        border-radius: 15px;

        padding: 1rem;
        width: 100%;

        max-width: fit-content;
    }

    table {
        margin: 0rem 0;

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
        color: white;
        
        white-space: nowrap;
        align-items: center;
        justify-content: space-between;
    }

    td {
        border-top: 1px solid #8689A2;
        
        max-width: 1000px;
        overflow: hidden;
        vertical-align: top;
        text-align: left;
    }

    #table-header {
        display: flex;
    }
    #table-title {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    #page {
        display: flex;
        justify-content: center;

        height: 2rem;
        padding-top: 0.5rem;
        padding-bottom: 1rem;
    }

    .page-number {
        margin-right: 6px;
    }

    .current-page {
        font-weight: bolder;
    }

    input {
        border: 0px;
        width: 100%;
        max-width: 50rem;
        margin-bottom: 1rem;
    }
    
    th:nth-child(0), td:nth-child(0) {
        min-width: 149px; /* Set a fixed width for the first column */
        max-width: 150px; /* Set a fixed width for the first column */
        word-wrap: break-word; /* Allow content to break within the max-width */
    }
    th:nth-child(1), td:nth-child(1) {
        min-width: 149px; /* Set a fixed width for the first column */
        max-width: 150px; /* Set a fixed width for the first column */
        word-wrap: break-word; /* Allow content to break within the max-width */
    }
    th:nth-child(2), td:nth-child(2) {
        min-width: 149px; /* Set a fixed width for the first column */
        max-width: 150px; /* Set a fixed width for the first column */
        word-wrap: break-word; /* Allow content to break within the max-width */
    }
    th:nth-child(3), td:nth-child(3) {
        min-width: 149px; /* Set a fixed width for the first column */
        max-width: 150px; /* Set a fixed width for the first column */
        word-wrap: break-word; /* Allow content to break within the max-width */
    }
    th:nth-child(4), td:nth-child(4) {
        min-width: 149px; /* Set a fixed width for the first column */
        max-width: 150px; /* Set a fixed width for the first column */
        word-wrap: break-word; /* Allow content to break within the max-width */
    }
    th:nth-child(5), td:nth-child(5) {
        min-width: 149px; /* Set a fixed width for the first column */
        max-width: 150px; /* Set a fixed width for the first column */
        word-wrap: break-word; /* Allow content to break within the max-width */
    }
    th:nth-child(6), td:nth-child(6) {
        min-width: 149px; /* Set a fixed width for the first column */
        max-width: 150px; /* Set a fixed width for the first column */
        word-wrap: break-word; /* Allow content to break within the max-width */
    }
    th:nth-child(7), td:nth-child(7) {
        min-width: 149px; /* Set a fixed width for the first column */
        max-width: 150px; /* Set a fixed width for the first column */
        word-wrap: break-word; /* Allow content to break within the max-width */
    }
    th:nth-child(8), td:nth-child(8) {
        min-width: 149px; /* Set a fixed width for the first column */
        max-width: 150px; /* Set a fixed width for the first column */
        word-wrap: break-word; /* Allow content to break within the max-width */
    }
</style>