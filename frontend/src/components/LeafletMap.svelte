<script>
// @ts-nocheck

    import { onMount, onDestroy } from 'svelte';
    import { browser } from '$app/environment';
	import PassangerList from './PassangerList.svelte';
    import { PUBLIC_BASE_URL } from '$env/static/public'
    import arrow from '$lib/assets/arrow.png'
    import marker from '$lib/assets/marker.png'
    import markerShadow from '$lib/assets/marker-shadow.png'

    export let flightNumber;
    let mapElement;
    let map;

    let showUsers = false;
    let passengers = [];
    let buttonRotation = 0;

    onMount(async () => {
        if(browser) {  
            const response = await fetch(PUBLIC_BASE_URL+`/vuelo/${flightNumber}`);
            const vuelo = await response.json();
            passengers = vuelo.passengers;
            const leaflet = await import('leaflet');

            map = leaflet.map(mapElement).setView([
                vuelo.airports[0].lat, vuelo.airports[0].lon], 
            13);

            leaflet.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png').addTo(map);
            
            var markerIcon = L.icon({
                iconUrl: marker,
                shadowUrl: markerShadow,
                iconSize: [50, 82],
                iconAnchor: [12,38]
            });

            markerIcon.options.iconSize = markerIcon.options.iconSize.map(size => size * 0.5);
            
            vuelo.airports.forEach(airport => {
                leaflet.marker([airport.lat, airport.lon], {icon: markerIcon}).addTo(map)
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

    function showUsersF() {
        showUsers = !showUsers;
        buttonRotation = (buttonRotation + 180)%360
    }
</script>

<body>
    <div id="button-container">
        <div>
            <a id="arrow" href="#/" on:click={showUsersF}>
                <img src={arrow} alt="arrow" style="transform: rotate({buttonRotation}deg);">
                Passengers
            </a>
        </div>
    </div>
    <div class="page-container">
        {#if showUsers}
            <PassangerList {flightNumber} {passengers}/>
        {/if}
        <div id='map'>
            <div bind:this={mapElement}></div>
        </div>
    </div>
</body>

<style>
    @import 'leaflet/dist/leaflet.css';

    #arrow {
        display: flex;
        color: white;
        text-decoration:none;
    }

    #arrow img {
        width: 4rem;
        margin-right: 0rem;
    }

    #button-container {
        display: flex; 
        justify-content: right;
        margin: -5px 15px;
        font-size: 35pt;
        text-align: center;
    }

    .page-container {
        display: flex;
        align-items: stretch;
        flex-direction: column;
        padding: 1rem;
    }

    #map div{
        height: 69vh; 
        border-radius: 10px;
    }

    body {
        overflow-x: hidden; /* Hide horizontal scrollbar */
    }
</style>