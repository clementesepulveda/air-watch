<script>
    // @ts-nocheck
	import { SyncLoader } from 'svelte-loading-spinners';

    export let title_keys;
    export let titles; // title_keys: title
    export let data; // [row1, row2]

    let current_sort_key = "";
    let sort_dir = 1;

    let loading = true;

    function sort_by(attribute) {
        if (attribute === current_sort_key) {
            sort_dir *= -1;
        } else {
            sort_dir = 1;
        }

        vuelos = vuelos.sort((a, b) => (a[attribute] > b[attribute]) ? sort_dir : -sort_dir);

        current_sort_key = attribute;
    }

    let page = 0;
    let pagination = 15;
</script>

<h1>Title</h1>

<div id="table">
    <table>
        <tr id="table-titles">
            {#each title_keys as title_key}
                <th>{titles[title_key]}<button on:click={()=>sort_by(title_key)}>s</button></th>
            {/each}
        </tr>
    {#if loading}
        <tr>
            <td colspan="8" class="center-loader">
                <div class="spinner">
                    <SyncLoader color="#F8F8F8"/>
                </div>
            </td>
        </tr>
    {:else}
            {#each data.slice(page*pagination, (page+1)*pagination) as item}
                <tr class="table-item" on:click={()=>console.log(vuelo)}>
                    <td>
                        <a href={`/map/${vuelo.flightNumber}`}>{vuelo.flightNumber}</a>
                    </td>
                    <td>{vuelo.origin}</td>
                    <td>{vuelo.destination}</td>
                    <td>{vuelo.airline}</td>
                    <td>{vuelo.averageAge.toFixed(2)} años</td>
                    <td></td>
                    <td>{vuelo.aircraftName}</td>
                    <td>{vuelo.passengersQty}</td>
                </tr>
            {/each}
    {/if}
    </table>
</div>

<style>
    h1 {
        font-size: 50pt;
        text-align: center;
    }

    #table {
        display: flex;
        justify-content: center;
    }

    .center-loader .spinner {
        margin: 30px auto;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    table {
        background-color: #303138;
        border-radius: 15px;
        margin: 2rem 1rem;

        font-family: arial, sans-serif;
        border-collapse: collapse;

        width: 100%;
        max-width: 90.8rem;

        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }
    
    th, td {
        text-align: left;
        padding: 18px;
    }

    th {
        border-bottom: 1px solid #8689A2;
        color: #8689A2;
    }

    td {
        border-top: 1px solid #8689A2;
    }

    th:nth-child(1) {
        width: 100px;
        overflow: hidden;
        background-color: rgba(150, 212, 212, 0.4);
    }


    #page {
        display: flex;
        justify-content: center;
        margin-bottom: 3rem;
    }

    .page-number {
        margin-right: 6px;
    }

    .current-page {
        font-weight: bolder;
    }
</style>