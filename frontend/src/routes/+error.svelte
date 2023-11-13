<script>
    // @ts-nocheck

	import { page } from '$app/stores';
    import Navbar from '../components/Navbar.svelte';
</script>

<Navbar />

<div class="container">
    <h1>{$page.status}: {$page.error.message}</h1>
</div>

<style>
    body {
        margin: 0;
        padding: 0;
    }

    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: calc(100vh - 100px); /* Adjust 64px based on your navbar height */
    }

    h1 {
        text-align: center;
        font-size: 60pt;
    }
</style>
