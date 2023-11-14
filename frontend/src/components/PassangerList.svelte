<script>
    // @ts-nocheck
    
    import { onMount } from 'svelte';
    import { PUBLIC_BASE_URL } from '$env/static/public'

	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    export let flightNumber;
    export let passengers;

    let current_sort_key = '';
    let sort_dir = 1;

    onMount(async () => {
        const response = await fetch(PUBLIC_BASE_URL+`/vuelo/${flightNumber}`);
        const vuelo = await response.json();
        passengers = vuelo.passengers;
    });

    function sort_by(attribute) {
        if (attribute === current_sort_key) {
            sort_dir *= -1;
        } else {
            sort_dir = 1;
        }

        passengers = passengers.sort((a, b) => (a[attribute] > b[attribute]) ? sort_dir : -sort_dir);
        current_sort_key = attribute;
    }
</script>

<body>
    <div id='users' transition:fly={{ duration: 300, x: 100, easing: quintOut }}>
        <h1>Passengers</h1>
        <table>
            <tr>
                <th></th>
                <th>Name<button on:click={()=>sort_by('firstName')}>s</button></th>
                <th>Seat Number<button on:click={()=>sort_by('lastName')}>s</button></th>
                <th>Age<button on:click={()=>sort_by('age')}>s</button></th>
                <th>Gender<button on:click={()=>sort_by('gender')}>s</button></th>
                <th>Weight<button on:click={()=>sort_by('weight(kg)')}>s</button></th>
                <th>Height<button on:click={()=>sort_by('height(cm)')}>s</button></th>
            </tr>
    
            {#each passengers as passenger}
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

</style>