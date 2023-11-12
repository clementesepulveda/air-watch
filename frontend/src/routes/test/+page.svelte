<script>
	import FlightsTable from "../../components/FlightsTable.svelte";

    const column_keys = ['key1', 'key2']
    const titles = {'key2': 'Title 2', 'key1': 'Title 1'}
    const data = [
        {'key1': 'name00123412341234123412341234123412341234123512351235', 'key2': 'name01'},
        {'key1': 'name10', 'key2': 'name11'},
        {'key1': 'name20', 'key2': 'name21'},
    ]
</script>

<FlightsTable 
    column_keys={column_keys} 
    titles={titles}
    data={data}
/>