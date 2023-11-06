<script>
        import Icon from "$lib/assets/triangle.png"

        let tri_class = 'tri-clicked-up';
        // function change_dir() {
        //     console.log("hello")
        //     if (tri_class == 'tri-clicked-up') {
        //         tri_class = 'tri-clicked-down'
        //     } else {
        //         tri_class = 'tri-clicked-up'
        //     }
        // }

</script>

<div id="navbar">
    <a href='/' id='app-name'>Air Watch</a>

    <div id="options">
        <a href='/vuelos'>Flights</a>
        <a href='/insights'>Insights</a>
    </div>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
    <!-- <img on:click={change_dir} src={Icon} alt="triangle" class={tri_class}> -->
</div>

<style>
    #navbar {
        /* background-color: red; */
        background-color: #303138;
        border-bottom: 1px #1f1f23 solid;
        box-shadow: 0px 2px 5px #1f1f23;

        padding: 2rem;
        margin-bottom: 1rem;
        /* height: 4rem; */
    }

    #app-name {
        display: inline-block;
    }

    #options {
        display: flex;
        float: right;
    }

    #options a {
        margin-left: 1rem;
    }

    a { 
        color: white;
    }

    img {
        width: 20px;
        /* background-color: green; */
    }

    :global(.tri-clicked-down) {
        transform: rotate(180deg);
    }

</style>