<script>
    // @ts-nocheck
    
    import { onMount, onDestroy } from 'svelte';
	import { createSearchStore, searchHandler } from '$lib/stores/search';
    import SortingIcon from './SortingIcon.svelte';

	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    export let flightNumber;
    export let passengers;
    let searchedPassengers= []
    let searchStore = null;
    let unsubscribe = null;

    let current_sort_key = '';
    let sort_dir = 1;
    const titles = [
        {name: "Name", key: "firstName", state: "all"},
        {name: "Seat Number", key: "seatNumber", state: "all"},
        {name: "Age", key: "age", state: "all"},
        {name: "Gender", key: "gender", state: "all"},
        {name: "Weight", key: "weight(kg)", state: "all"},
        {name: "Height", key: "height(cm)", state: "all"},
    ]

    let loading = true;
    let page = 0;
    const pagination = 15;
    let pages = []

    onMount(async () => {
        loading = true;
        
        searchedPassengers = passengers.map( passenger => ({
            ...passenger,
            searchTerms: `${passenger.firstName} ${passenger.lastName}`
        }))
        searchStore = createSearchStore(searchedPassengers);
        unsubscribe = searchStore.subscribe(model => searchHandler(model))
        sort_by("lastName")

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
        $searchStore.data = $searchStore.data.sort((a, b) => (a["lastName"] < b["lastName"]) ? 1 : -1);
        $searchStore.data = $searchStore.data.sort((a, b) => (a[attribute] > b[attribute]) ? sort_dir : -sort_dir);
        
        current_sort_key = attribute;
    }
    

    function change_page(dir) {
        if (0 <= page + dir && page + dir < $searchStore.data.length / pagination) {
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
        let maxNumber = $searchStore.data.length / pagination;
        let result = [];

        if (maxNumber <= pagination) {
            for (let i = 0; i < maxNumber; i++) {
                result.push(i);
            }
            pages = result;
            return result;
        }

        let start = Math.max(0, page - 2);
        let end = Math.min(maxNumber, page + 2);

        if (page <= 3) {
            end = 5;
        } else if (page >= maxNumber - 2) {
            start = maxNumber - 4;
        }

        for (let i = start; i <= end; i++) {
            result.push(i);
        }

        pages = result;
    }
</script>

<body>
    <div id='users' transition:fly={{ duration: 300, x: 100, easing: quintOut }}>
        <h1>Passengers</h1>

        {#if !loading}
        
        
<div id="table-container">
    <div id="table">
        <input type="search" placeholder="Search passenger" bind:value={$searchStore.search}>
        <table>
            <tr>
                <th></th>
                
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
    
            {#each $searchStore.filtered.slice(page*pagination, (page+1)*pagination) as passenger}
            <tr>
                <td id="img-container"><img src={passenger.avatar} alt="passanger"></td>
                <td>{passenger.firstName} {passenger.lastName}</td>
                <td>{passenger.seatNumber}</td>
                <td>{passenger.age} years</td>
                <td>{passenger.gender}</td>
                <td>{passenger['weight(kg)']} kg</td>
                <td>{passenger['height(cm)']} cm</td>
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
    </div>
</div>
        {/if}
    </div>
</body>


<style>
    h1 {
        text-align: center;
    }

    #users {
        background-color: #303138; 
        border-radius: 10px;

        position: absolute;
        z-index: 9999;
        right:10px;
        max-width: 100%;
        overflow-x: hidden;
    }

    table {
        max-width: 48rem;
    }

    img {
        border-radius: 5rem;
        width: 80px;
    }

    #img-container {
        width: 50px;
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

    input {
        border: 0px;
        width: 100%;
        max-width: 50rem;
        margin-bottom: 1rem;
    }

    
    

</style>