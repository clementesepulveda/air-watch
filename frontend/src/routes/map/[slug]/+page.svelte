<script>
    import LeafletMap from './LeafletMap.svelte';
    
    export let data;
</script>

<main>
    <LeafletMap flightNumber={data.flightNumber}/>
</main>