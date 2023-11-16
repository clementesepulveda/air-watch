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
    let filteredData = []
    let page = 0;
    let pagination = 15;
    let pages = []

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

    onMount(async () => {
        loading = true;

        const response = await fetch(PUBLIC_BASE_URL+"/vuelos");
        const vuelos = await response.json();
        
        searchedFlights = vuelos.map( vuelo => ({
            ...vuelo,
            searchTerms:  `${vuelo.city_y} ${vuelo.origin}`,
            searchTerms2: `${vuelo.city_x} ${vuelo.destination}`
        }))
        searchStore = createSearchStore(searchedFlights);
        unsubscribe = searchStore.subscribe(model => searchHandler(model))
        sort_by("year")
        updatePages();
        loading = false;
    });

    onDestroy(() => {
        if (unsubscribe !== null) {
            unsubscribe();
        }
    })

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

        $searchStore.data = $searchStore.data.sort((a, b) => (a["flightNumber"] > b["flightNumber"]) ? 1 : -1);
        $searchStore.data = $searchStore.data.sort((a, b) => (a["month"] > b["month"]) ? 1 : -1);
        $searchStore.data = $searchStore.data.sort((a, b) => (a["year"] > b["year"]) ? 1 : -1);
        $searchStore.data = $searchStore.data.sort((a, b) => (a[attribute] > b[attribute]) ? sort_dir : -sort_dir);

        current_sort_key = attribute;
    }

    function change_page(dir) {
        if (0 <= page + dir && page + dir < $searchStore.filtered.length / pagination) {
            page += dir
            document.body.scrollIntoView();
            updatePages();
        }
    }


    function change_to_page(p) {
        if (p != page) {
            page = p
            document.body.scrollIntoView();
            updatePages();
        }
    }

    function updatePages() {
        let maxNumber = $searchStore.filtered.length / pagination;
        pages = [];

        if (maxNumber <= pagination) {
            for (let i = 0; i < maxNumber; i++) {
                pages.push(i);
            }
            return pages;
        }

        let start = Math.max(0, page - 2);
        let end = Math.min(maxNumber, page + 2);

        if (page <= 3) {
            end = 5;
        } else if (page >= maxNumber - 2) {
            start = maxNumber - 4;
        }

        for (let i = start; i <= end; i++) {
            pages.push(i);
        }

        return pages;
    }

    $: {
        $searchStore
        if ($searchStore && $searchStore.filtered) {
            change_to_page(0);
            updatePages();
        }
    }

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
        <input type="search" placeholder="Search origin" bind:value={$searchStore.search}>
        <input type="search" placeholder="Search destination" bind:value={$searchStore.search2}>
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
            
            <div class="pagination">
                <!-- svelte-ignore a11y-invalid-attribute -->
                <a href={page==0? "#/":"#"} on:click={()=>change_page(-1)}>&laquo;</a>
                {#each pages as index}
                    <!-- svelte-ignore a11y-invalid-attribute -->
                    <a href={page==index? "#/":"#"} class={index==page ? "active" : ""} on:click={()=>change_to_page(index)}>{index+1}</a>
                {/each}
                <!-- svelte-ignore a11y-invalid-attribute -->
                <a href="#"  on:click={()=>change_page(1)}>&raquo;</a>
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