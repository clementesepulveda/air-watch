/** @type {import('./$types').PageLoad} */
export function load({ params }) {
    return {
        flightNumber: params.slug
    }
}