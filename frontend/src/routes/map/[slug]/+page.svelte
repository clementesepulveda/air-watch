<script>
    import LeafletMap from './LeafletMap.svelte';
    
    export let data;

    console.log(data)
</script>

<main>
    <LeafletMap flightNumber={data.flightNumber}/>
</main>