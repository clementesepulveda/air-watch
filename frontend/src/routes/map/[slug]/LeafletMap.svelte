<script>
// @ts-nocheck

    import { onMount, onDestroy } from 'svelte';
    import { browser } from '$app/environment';
    import { PUBLIC_BASE_URL } from '$env/static/public'

    export let flightNumber;
    let mapElement;
    let map;

    let passengers = [];
    let current_sort_key = '';
    let sort_dir = 1;

    onMount(async () => {
        if(browser) {  
            const response = await fetch(PUBLIC_BASE_URL+`/vuelo/${flightNumber}`);
            const vuelo = await response.json();
            console.log(vuelo)
            passengers = vuelo.passengers

            const leaflet = await import('leaflet');

            // TODO
            map = leaflet.map(mapElement).setView([
                vuelo.airports[0].lat, vuelo.airports[0].lon], 
            13);

            leaflet.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png').addTo(map);
            
            vuelo.airports.forEach(airport => {
                leaflet.marker([airport.lat, airport.lon]).addTo(map)
                    .bindPopup(`Airport: ${airport.name}<br>City: ${airport.city}.<br>Country: ${airport.country}`)
            });

            let pointList = vuelo.airports.map(airport => [airport.lat, airport.lon])

            var line = new L.Polyline(pointList, {
                color: 'red',
                weight: 20,
                opacity: 0.7,
                smoothFactor: 1
            }).bindPopup(`Flight Number: ${vuelo.flight.flightNumber}.<br> Airline: ${vuelo.flight.airline}`)

            line.addTo(map);
            map.fitBounds(line.getBounds());
        }
    });

    onDestroy(async () => {
        if(map) {
            map.remove();
        }
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


<div class="page-container">
    <div id='map'>
        <div bind:this={mapElement}></div>
    </div>
    <div id='users'>
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
                <td><img src={passenger.avatar} alt="passanger"></td>
                <td>{passenger.firstName} {passenger.firstName}</td>
                <td>{passenger.seatNumber}</td>
                <td>{passenger.age}</td>
                <td>{passenger.gender}</td>
                <td>{passenger['weight(kg)']}</td>
                <td>{passenger['height(cm)']}</td>
            </tr>
            {/each}
        </table>
    </div>
</div>

<style>
    @import 'leaflet/dist/leaflet.css';
    #map div{
        width: 800px;
        height: 800px; 
        border-radius: 10px;
        margin: 1rem;
    }

    img {
        border-radius: 5rem;
    }

    table {
        max-width: 48rem;
    }

    .page-container {
        display: flex;
    }

</style>