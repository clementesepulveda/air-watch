<script>
    // @ts-nocheck
    import { onMount } from 'svelte';
    import { PUBLIC_BASE_URL } from '$env/static/public'

    let vuelos = []

    let page = 0;
    let pagination = 15;

    let current_sort_key = "";
    let sort_dir = 1;

    function sort_by(attribute) {
        if (attribute === current_sort_key) {
            sort_dir *= -1;
        } else {
            sort_dir = 1;
        }

        vuelos = vuelos.sort((a, b) => (a[attribute] > b[attribute]) ? sort_dir : -sort_dir);

        current_sort_key = attribute;
    }

    function change_page(dir) {
        if (0 <= page + dir*pagination && page + dir*pagination < vuelos.length) {
            page += dir*pagination
        }
    }

    onMount(async () => {
        const response = await fetch(PUBLIC_BASE_URL+"/vuelos");
        vuelos = await response.json();
        console.log(vuelos)
    });

</script>

<h1>Tarea 3</h1>

<table>
    <tr>
        <th>Origen <button on:click={()=>sort_by('origin')}>s</button></th>
        <th>Destino <button on:click={()=>sort_by('destination')}>s</button></th>
        <th>Aerolínea <button on:click={()=>sort_by('airline')}>s</th>
        <th>Edad Promedio <button on:click={()=>sort_by('averageAge')}>s</th>
        <th>Distancia Recorrida <button on:click={()=>sort_by('dist_recorrida')}>s</th>
        <th>Nombre Avión <button on:click={()=>sort_by('aircraftName')}>s</th>
        <th>Cantidad Pasajeros <button on:click={()=>sort_by('passengersQty')}>s</th>
    </tr>
    {#each vuelos.slice(page, page+pagination) as vuelo}
        <tr on:click={()=>console.log(vuelo)}>
            <th>{vuelo.origin}</th>
            <th>{vuelo.destination}</th>
            <th>{vuelo.airline}</th>
            <th>{vuelo.averageAge.toFixed(2)}</th>
            <th></th>
            <th>{vuelo.aircraftName}</th>
            <th>{vuelo.passengersQty}</th>
        </tr>
    {/each}
</table>

<div id="page">
    <button on:click={()=>change_page(-1)}>left</button>
    {#each Array.from({length: 10}, (_, i) => i + page/pagination).filter(v=> v >= 0) as page_number}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div on:click={()=>page=page_number*pagination}>{page_number+1}</div>
    {/each}
    <button on:click={()=>change_page(1)}>right</button>
</div>

<style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }
    
    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }
    
    tr:nth-child(even) {
      background-color: #dddddd;
    }

    #page {
        display: flex;
    }

    div {
        margin-right: 6px;
    }
</style>