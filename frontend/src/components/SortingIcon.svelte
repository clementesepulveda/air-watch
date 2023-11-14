<script>
    // @ts-nocheck
    
    export let onClickFunction;
    export let data;
</script>

<a href="#/" on:click={onClickFunction} class="wrapper">
    <div class={`top-triangle ${data.state === "down" ? 'top-invisible' : ''}`}></div>
    <div class={`bottom-triangle ${data.state === "up" ? 'bottom-invisible' : ''}`}></div>
</a>

<style>
    .wrapper {
        display:flex;
        flex-direction:column;
        padding:5px;
    }

    :global(.top-triangle) {
        width: 0; 
        height: 0; 
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
        
        border-bottom: 10px solid #8689A2;
        margin-bottom:3px;
    }

    :global(.bottom-triangle) {
        width: 0; 
        height: 0; 
        
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
        border-top: 10px solid #8689A2;
    }

    :global(.top-invisible) {
        border-bottom: 10px solid transparent;
    }

    :global(.bottom-invisible) {
        border-top: 10px solid transparent;
    }

</style>