<script>
    // @ts-nocheck

    export let column_keys;
    export let titles; // column_keys: title
    export let data; // [{colum_key: data_1, ..}]

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

    let page = 0;
    let pagination = 15;
</script>

<main>
    <div id="table">
        <table>
            <tr id="table-titles">
                {#each column_keys as column}
                    <th>{titles[column]}<button on:click={()=>sort_by(column)}>s</button></th>
                {/each}
            </tr>
            {#each data.slice(page*pagination, (page+1)*pagination) as item}
                <tr class="table-item" on:click={()=>console.log(item)}>
                    {#each column_keys as column}
                        <td>{item[column]}</td>
                    {/each}
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
    </div>
</main>

<style>
    main {
        display: flex;
        justify-content: center;

        width: 100%;
        background-color: purple;
    }

    #table {
        /* background-color: #303138;  */
        background-color: red;

        /* display: flex;
        flex-direction: column;
        justify-content: center; */

        /* border-radius: 15px; */
        width: 100%;
        /* max-width:fit-content; */
        /* margin: 1rem; */
    }

    table {
        background-color: green;

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
        
        white-space: nowrap;
    }

    td {
        border-top: 1px solid #8689A2;
        
        max-width: 1000px;
        overflow: hidden;
    }


    
    #page {
        display: flex;
        justify-content: center;

        height: 2rem;
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        /* background-color: red; */
    }

    .page-number {
        margin-right: 6px;
    }

    .current-page {
        font-weight: bolder;
    }
</style>