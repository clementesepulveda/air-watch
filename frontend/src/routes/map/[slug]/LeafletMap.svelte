<script>
// @ts-nocheck

    import { onMount, onDestroy } from 'svelte';
    import { browser } from '$app/environment';
    import { PUBLIC_BASE_URL } from '$env/static/public'

    export let flightNumber;
    let mapElement;
    let map;

    onMount(async () => {
        if(browser) {  

            const response = await fetch(PUBLIC_BASE_URL+"/vuelos");
            const vuelos = await response.json();
            console.log(vuelos)

            let index = 0;
            for (let i = 0; i < vuelos.length; i++) {
                const element = vuelos[i];
                if (element.flightNumber == flightNumber) {
                    index = i;
                    break;
                }
            }

            const leaflet = await import('leaflet');

            map = leaflet.map(mapElement).setView([vuelos[index].lat_x, vuelos[index].lon_x], 13);

            leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            leaflet.marker([vuelos[index].lat_x, vuelos[index].lon_x]).addTo(map)
                .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
                // .openPopup();
            leaflet.marker([vuelos[index].lat_y, vuelos[index].lon_y]).addTo(map)
                .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
                // .openPopup();

            var pointA = new L.LatLng(vuelos[index].lat_x, vuelos[index].lon_x);
            var pointB = new L.LatLng(vuelos[index].lat_y, vuelos[index].lon_y);
            var pointList = [pointA, pointB];

            var firstpolyline = new L.Polyline(pointList, {
                color: 'red',
                weight: 20,
                opacity: 0.7,
                smoothFactor: 1
            }).bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
                // .openPopup();

            firstpolyline.addTo(map);
        }
    });

    onDestroy(async () => {
        if(map) {
            map.remove();
        }
    });
</script>


<main>
    <div bind:this={mapElement}></div>
</main>

<style>
    @import 'leaflet/dist/leaflet.css';
    main div {
        height: 800px;
    }
</style>