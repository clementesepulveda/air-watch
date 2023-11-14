<script>
	import Navbar from '../../../components/Navbar.svelte';
    import LeafletMap from '../../../components/LeafletMap.svelte';
    
    export let data;
</script>

<main>
    <Navbar />
    <LeafletMap flightNumber={data.flightNumber}/>
</main>