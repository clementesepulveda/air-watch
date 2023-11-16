import { writable } from "svelte/store"

export const createSearchStore = (data: any) => {
    const { subscribe, set, update} = writable({
        data: data,
        filtered: data,
        search: '',
        search2: '',
    })

    return {
        subscribe,
        set,
        update
    }
}

export const searchHandler = (store: { search: string; search2: string; filtered: any; data: any[] }) => {
    
    const searchTerm = (store.search?store.search:'').toLowerCase() || "";
    store.filtered = store.data.filter(item => {
        return (item.searchTerms?item.searchTerms:'').toLowerCase().includes(searchTerm)
    })
    
    const searchTerm2 = (store.search2?store.search2:'').toLowerCase() || "";
    store.filtered = store.filtered.filter((item: { searchTerms2: string }) => {
        return (item.searchTerms2?item.searchTerms2:'').toLowerCase().includes(searchTerm2)
    })
}